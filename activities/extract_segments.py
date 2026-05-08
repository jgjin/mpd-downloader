from urllib.parse import urljoin

from mpd_parser.models.composite_tags import Representation as RepresentationTag
from mpd_parser.parser import Parser
from temporalio import activity

from schemas.video import ExtractedSegments, SegmentToDownload, VideoToDownload
from storage.get_storage import get_storage


@activity.defn
async def extract_segments(
    video_to_download: VideoToDownload,
) -> ExtractedSegments:
    video_id = video_to_download.id
    mpd_path = video_to_download.mpd_path

    mpd_content = get_storage().read_file(mpd_path)
    if not mpd_content:
        raise ValueError(f"no content at {mpd_path}")
    mpd = Parser.from_string(mpd_content)

    if not mpd.base_urls:
        raise ValueError(f"no base URLs found in {mpd_path}")
    base_url = mpd.base_urls[0].text

    all_representations = []
    for period in mpd.periods:
        for adaptation_set in period.adaptation_sets:
            all_representations.extend(adaptation_set.representations)

    video_reps = [r for r in all_representations if r.mime_type.startswith("video")]
    best_video_rep = max(video_reps, key=lambda r: r.bandwidth, default=None)
    if not best_video_rep:
        raise ValueError(f"no video representation found in {mpd_path}")

    audio_reps = [r for r in all_representations if r.mime_type.startswith("audio")]
    best_audio_rep = max(audio_reps, key=lambda r: r.bandwidth, default=None)
    if not best_audio_rep:
        raise ValueError(f"no audio representation found in {mpd_path}")

    return ExtractedSegments(
        video_id=video_id,
        video_segments=[
            SegmentToDownload(
                video_id=video_id,
                content_type="video",
                index=index,
                download_url=download_url,
            )
            for index, download_url in enumerate(
                extract_segment_download_urls_from_rep(best_video_rep, base_url)
            )
        ],
        audio_segments=[
            SegmentToDownload(
                video_id=video_id,
                content_type="audio",
                index=index,
                download_url=download_url,
            )
            for index, download_url in enumerate(
                extract_segment_download_urls_from_rep(best_audio_rep, base_url)
            )
        ],
    )


def extract_segment_download_urls_from_rep(
    rep: RepresentationTag, base_url: str
) -> list[str]:
    if not rep.segment_lists:
        raise ValueError(f"no segment lists found in representation {rep.id}")
    segment_list = rep.segment_lists[0]

    if not segment_list.initializations:
        raise ValueError(f"no initializations found in representation {rep.id}")
    initialization = segment_list.initializations[0]

    if not segment_list.segment_urls:
        raise ValueError(f"no segment URLs found in representation {rep.id}")
    segment_urls = segment_list.segment_urls

    segment_download_urls = [urljoin(base_url, initialization.source_url)]
    for segment_url in segment_urls:
        segment_download_urls.append(urljoin(base_url, segment_url.media))

    return segment_download_urls

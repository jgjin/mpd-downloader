from temporalio.common import RetryPolicy

standard_retry_policy = RetryPolicy(maximum_attempts=3)

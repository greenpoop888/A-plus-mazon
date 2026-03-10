resource "aws_cloudwatch_event_rule" "every_min" {
  name                = "report-trigger-1min"
  schedule_expression = "cron(* * * * ? *)"
}

resource "aws_cloudwatch_event_target" "target_1min" {
  rule = aws_cloudwatch_event_rule.every_min.name
  arn  = aws_lambda_function.report_dispatcher.arn
  input_transformer {
    input_paths    = { time = "$.time" }
    input_template = "{\"frequency\": \"minute\", \"scheduled_at\": <time>}"
  }
}

resource "aws_cloudwatch_event_rule" "hourly" {
  name                = "report-trigger-hourly"
  schedule_expression = "cron(0 * * * ? *)"
}

resource "aws_cloudwatch_event_target" "target_hourly" {
  rule = aws_cloudwatch_event_rule.hourly.name
  arn  = aws_lambda_function.report_dispatcher.arn
  input_transformer {
    input_paths    = { time = "$.time" }
    input_template = "{\"frequency\": \"hour\", \"scheduled_at\": <time>}"
  }
}

resource "aws_cloudwatch_event_rule" "daily" {
  name                = "report-trigger-daily"
  schedule_expression = "cron(0 0 * * ? *)"
}

resource "aws_cloudwatch_event_target" "target_daily" {
  rule = aws_cloudwatch_event_rule.daily.name
  arn  = aws_lambda_function.report_dispatcher.arn
  input_transformer {
    input_paths    = { time = "$.time" }
    input_template = "{\"frequency\": \"day\", \"scheduled_at\": <time>}"
  }
}

resource "aws_cloudwatch_event_rule" "weekly" {
  name                = "report-trigger-weekly"
  schedule_expression = "cron(0 0 ? * MON *)"
}

resource "aws_cloudwatch_event_target" "target_weekly" {
  rule      = aws_cloudwatch_event_rule.weekly.name
  arn       = aws_lambda_function.report_dispatcher.arn
  input_transformer {
    input_paths    = { time = "$.time" }
    input_template = "{\"frequency\": \"week\", \"scheduled_at\": <time>}"
  }
}

resource "aws_cloudwatch_event_rule" "monthly" {
  name                = "report-trigger-monthly"
  schedule_expression = "cron(0 0 1 * ? *)"
}

resource "aws_cloudwatch_event_target" "target_monthly" {
  rule      = aws_cloudwatch_event_rule.monthly.name
  arn       = aws_lambda_function.report_dispatcher.arn
  input_transformer {
    input_paths    = { time = "$.time" }
    input_template = "{\"frequency\": \"month\", \"scheduled_at\": <time>}"
  }
}

resource "aws_lambda_permission" "allow_events" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.report_dispatcher.function_name
  principal     = "events.amazonaws.com"
}

resource "aws_lambda_event_source_mapping" "sqs_to_worker" {
  event_source_arn = aws_sqs_queue.report_queue.arn
  function_name    = aws_lambda_function.worker.arn
  batch_size       = 1
}
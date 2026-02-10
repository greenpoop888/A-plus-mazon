# 1. API Gateway 基礎設定
resource "aws_api_gateway_rest_api" "inventory_api" {
  name = var.apigateway_name

  endpoint_configuration {
    types = ["REGIONAL"] # 已修正拼字
  }
}

# 2. API Key 與使用計畫 (Usage Plan)
resource "aws_api_gateway_api_key" "client_key" {
  name = var.apigateway_apikey_name
}

resource "aws_api_gateway_usage_plan" "usage_plan" {
  name = "StandardPlan"

  api_stages {
    api_id = aws_api_gateway_rest_api.inventory_api.id
    stage  = aws_api_gateway_stage.prod.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.client_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.usage_plan.id
}

# 3. 定義路徑: /inventory
resource "aws_api_gateway_resource" "inventory" {
  rest_api_id = aws_api_gateway_rest_api.inventory_api.id
  parent_id   = aws_api_gateway_rest_api.inventory_api.root_resource_id
  path_part   = "inventory"
}

# 4. 定義方法: GET /inventory
resource "aws_api_gateway_method" "get_inventory" {
  rest_api_id      = aws_api_gateway_rest_api.inventory_api.id
  resource_id      = aws_api_gateway_resource.inventory.id
  http_method      = "GET"
  authorization    = "NONE"
  api_key_required = true 
}

# 5. 整合 Lambda
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.inventory_api.id
  resource_id             = aws_api_gateway_resource.inventory.id
  http_method             = aws_api_gateway_method.get_inventory.http_method
  integration_http_method = "POST" 
  type                    = "AWS_PROXY" 
  uri                     = aws_lambda_function.inventory_api.invoke_arn # 已修正名稱
}

# 6. 部署與 Stage
resource "aws_api_gateway_deployment" "example" {
  rest_api_id = aws_api_gateway_rest_api.inventory_api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.inventory.id,
      aws_api_gateway_method.get_inventory.id,
      aws_api_gateway_integration.lambda_integration.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.example.id
  rest_api_id   = aws_api_gateway_rest_api.inventory_api.id
  stage_name    = "prod"
}

# 7. 權限授權：只允許此 API Gateway 存取 Lambda
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.inventory_api.function_name
  principal     = "apigateway.amazonaws.com"

  # 限制只有這個 API Gateway 實例的 prod stage 可以呼叫
  source_arn = "${aws_api_gateway_rest_api.inventory_api.execution_arn}/*/*"
}

output "api_url" {
  value = "${aws_api_gateway_stage.prod.invoke_url}/inventory"
}
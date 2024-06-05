# serverless-todo
このプロジェクトはAWSのSAMフレームワークを使用して構築されたサーバーレスアプリケーションです。このアプリケーションは、ユーザー登録、Todoリストの管理、およびタスクの管理を行います。フロントエンドはReactで構築され、S3とCloudFrontを使用してホスティングされます。バックエンドはDynamoDBを使用してデータを保存し、API GatewayとLambdaを使用してAPIを提供します。

以下の手順に従って、このプロジェクトをクローンし、デプロイしてください。

## 前提条件

	•	AWS CLIがインストールされていること
	•	SAM CLIがインストールされていること
	•	Node.jsおよびnpmがインストールされていること
	•	AWSアカウントを持っていること

## クローンからデプロイまでの手順

1.	リポジトリのクローン:
```
git clone https://github.com/your-repository/todo-app.git
cd todo-app
```
2.	バックエンドのセットアップ:
```
cd ../backend
sam build
sam deploy --guided
```
	•	sam deploy --guidedを実行すると、いくつかの設定オプションが表示されます。適切な値を入力してください。例えば：
	•	Stack Name: todo-app
	•	AWS Region: ap-northeast-1 (例として東京リージョン)
	•	Confirm changes before deploy: y
	•	Allow SAM CLI IAM role creation: y

3.	フロントエンドのセットアップ:

```
cd frontend
npm install
```
    src/api/api.jsxのエンドポイントをデプロイしたAPI Gatewayのエンドポイントに変更する
```
npm run build
```

4.	S3バケットの作成:
    •	AWSコンソールでS3バケットを作成します。バケット名は任意ですが、一意である必要があります。
    •	バケットのプロパティで「Static website hosting」を有効にし、index.htmlをエントリポイントとして指定します。
5.	ビルドしたフロントエンドをS3にアップロード:
```
aws s3 sync dist/ s3://your-s3-bucket-name
```
6.	CloudFrontディストリビューションの作成:
    •	AWSコンソールでCloudFrontディストリビューションを作成し、先ほど作成したS3バケットをオリジンとして設定します。
    •   API Gatewayのオリジンを追加。パスを/apiにする
    •   ビヘイビアに/api/*でAPI Gatewayにアクセスするようにする。API Gateway行きはキャッシュを使用しない設定をする
7.	API GatewayのCORS設定:
	•	AWSコンソールでAPI Gatewayに移動し、デプロイされたAPIの各メソッド（GET、POST、OPTIONSなど）に対してCORSを設定します。
8.	Lambda関数の設定確認:
	•	デプロイ後、Lambda関数が適切に設定されていることを確認します。
9.	フロントエンドアプリのCloudFront設定:
	•	CloudFrontディストリビューションのビヘイビア設定で、API GatewayのURLへのアクセスを許可します。
10.	アプリケーションのテスト:
	•	CloudFrontのURLにアクセスして、アプリケーションが正しく動作することを確認します。

## デプロイ後の管理
	•	リソースの削除:
	•	デプロイしたリソースを削除するには、以下のコマンドを実行します。
 ```
aws cloudformation delete-stack --stack-name todo-app
 ```
 	•	ログの確認:
	•	Lambda関数のログは、CloudWatch Logsで確認できます。

## トラブルシューティング

.env: no such file or directory

.env ファイルがないので環境変数の一覧を参考に作成しましょう

docker daemon is not running

Docker Desktop が起動できていないので起動させましょう

Ports are not available: address already in use

別のコンテナもしくはローカル上ですでに使っているポートがある可能性があります

下記記事を参考にしてください

コンテナ起動時に Ports are not available: address already in use が出た時の対処法について

Module not found

make build

を実行して Docker image を更新してください
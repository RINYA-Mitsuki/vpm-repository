# Mitsuboshi_Studio VPM Repository

Unity Editor ツールを VRChat Creator Companion (VCC) で導入・更新するための共通 Listing です。

## VCCに追加

### [▶ クリックしてVCCを開く](https://rinya-mitsuki.github.io/vpm-repository/add.html)

リンクをクリックするとVCCが開きます。ブラウザーの確認で「開く」を選び、VCC内でリポジトリの追加を確定してください。自動で開かない場合は、リンク先の「VCCを開いて追加」を押してください。

登録後はプロジェクトの Manage Project から Unity Power Rename を追加できます。beta版の表示には **Show Pre-Release Packages** を有効にしてください。

最初のパッケージは **Unity Power Rename 1.0.0-beta.1**。試験版を表示するには VCC の Show Pre-Release Packages を有効にしてください。プロジェクトの Manage Project から追加・更新できます。旧版スクリプトを使用中の場合は、パッケージ README の移行手順を先に確認してください。

## 運用

- `source.json` にパッケージリポジトリを追加。
- 毎時17分（UTC）に公開 Release を読み取り、ZIP と manifest を検証し、index.json を GitHub Pages に配置。
- 即時反映は Actions → **Build VPM listing** → Run workflow。
- GitHub の schedule は遅延する場合があり、公開リポジトリで60日間活動がないと無効化されます。必要時に再有効化してください。
- パッケージの公開版が欠落／変更された場合、更新を失敗させて既存 Listing を保持します。
- 新しいツールの追加方法・命名・版管理は [標準仕様](docs/STANDARD.md) を参照。

## 初期設定

Settings → Pages → Build and deployment → Source を **GitHub Actions** に設定します。パッケージの初回 Release を公開した後に Listing の workflow を実行してください。リポジトリ横断の書き込み用 PAT は不要です。

## 利用上の注意・サポート方針

掲載ツールは作者が完全に個人用として作成したものを現状のまま公開しています。利用はご自身の判断と責任で行ってください。動作・品質は保証せず、サポート・不具合修正・機能追加・問い合わせへの回答はお約束しません。**利用したことによる苦情は一切受け付けません。** 各パッケージの LICENSE と注意事項を確認し、利用前にプロジェクトをバックアップしてください。

## 検証状況

Release と Listing の公開、匿名ダウンロード、SHA-256 の一致を確認済みです。詳細と未検証項目は [検証結果](docs/VERIFICATION.md) を参照してください。

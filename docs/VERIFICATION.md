# VPM 構築・検証結果

確認日: 2026-09-16

## 公開結果

- 共通Listing: https://rinya-mitsuki.github.io/vpm-repository/index.json
- VCC起動リンク: https://rinya-mitsuki.github.io/vpm-repository/add.html
- 対象: Unity Editorツール9件、すべて正式版 `1.0.0`
- CGE-ND: ユーザー指定により対象外
- GitHub Actions: Release作成、Listing生成、GitHub Pages配信に成功
- Listing生成結果: 9パッケージ・10バージョン（Unity Power Renameの旧beta.1を履歴として保持）

## 確認済み

| 項目 | 結果 |
|---|---|
| 元コードの保持 | 各パッケージのEditor用C#は指定フォルダーの元ファイルを内容変更なしで収録 |
| C#コンパイル | 9ツールすべてUnity 2022.3.22f1の参照ライブラリで成功 |
| VRChat依存 | Better Animator Transition CopyとVRC Contact CounterをVRChat SDK Base 3.10.4でコンパイル確認 |
| パッケージ検証 | manifest、SemVer、Editor限定assembly、GUID、決定的ZIP生成のテストに成功 |
| Release | 9件すべて `v1.0.0` を正式版として公開し、ZIP・package.json・SHA256SUMSを添付 |
| Listing | ReleaseとmanifestとZIPを検証し、10バージョンをGitHub Pagesへ配信 |
| Unity Power Rename | ユーザーによるVCC登録、Unity起動、実動作確認済み |

## 未検証

Unity Power Rename以外の8ツールは、Unity Editor内での操作・実動作を未検証です。正式版は配布区分を表し、全環境での動作を保証するものではありません。各READMEの注意事項に従い、導入前にプロジェクトをバックアップしてください。

## 自動化

各パッケージはmainまたは対応する `v{version}` タグからReleaseを生成します。公開済みアセットは上書きしません。共通Listingは毎時17分（UTC）に確認し、公開版の欠落や内容変更を検出した場合は以前のListingを保持して失敗します。

ツール本体、VPMパッケージ化、配布用リポジトリおよび自動化環境は、すべてAIを利用して制作しています。


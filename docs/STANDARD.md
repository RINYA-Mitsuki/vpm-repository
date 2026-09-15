# Mitsuboshi_Studio VPM 標準仕様

状態: Unity Power Rename v7 の VPM 化仕様。実行結果は VERIFICATION.md を参照。

## 1. 管理単位
- Editor ツールごとに独立した GitHub リポジトリを使用する。
- 共通リポジトリ `vpm-repository` は配布一覧と運用仕様を管理する。
- 所有者: RINYA-Mitsuki。既存リポジトリの公開範囲は変更しない。
- パッケージ ID: `com.mitsuboshi-studio.unity-power-rename`。以後変更しない。
- 表示ブランドは `Mitsuboshi_Studio`、表示名は `Unity Power Rename`。

## 2. ディレクトリ
```text
unity-power-rename/
  .github/workflows/validate.yml
  .github/workflows/release.yml
  Packages/com.mitsuboshi-studio.unity-power-rename/
    package.json
    Editor/
      MitsuboshiStudio.UnityPowerRename.Editor.asmdef
      ...既存コードと .meta
    README.md
    CHANGELOG.md
    LICENSE.md
  scripts/
  tests/
  README.md
vpm-repository/
  .github/workflows/listing.yml
  source.json
  scripts/
  tests/
  docs/STANDARD.md
```

既存 .meta の GUID は保持する。Editor 用 assembly は includePlatforms を Editor に限定する。既存 asmdef や依存関係を確認してから分割を行う。Unity の対象版は 2022.3。実機検証状況は VERIFICATION.md に記録する。SDK に依存しないツールには VRChat SDK の依存を追加しない。

## 3. 命名
- GitHub リポジトリとパッケージ ID の末尾: 小文字 kebab-case。
- C# の新規 namespace: `MitsuboshiStudio.UnityPowerRename`。既存公開 API の名前変更は移行リスクを確認してから行う。
- assembly: `MitsuboshiStudio.UnityPowerRename.Editor`。
- ZIP: `{package-id}-{version}.zip`。ZIP 直下に package.json を配置する。
- タグ: `v{version}`。package.json と完全一致させる。

## 4. バージョニング
SemVer 2.0.0 を採用する。破壊的変更は MAJOR、互換性のある機能追加は MINOR、不具合修正は PATCH。初回 VPM 化の番号は既存配布版の番号を確認して決める。未検証版は `-beta.1` 等を付ける。公開済みタグ、ZIP、同一バージョンの内容は上書きしない。不具合は新しい PATCH で直す。旧版の Release と Listing エントリーを維持する。

## 5. パッケージ Release
1. PR で manifest、SemVer、GUID 重複、必要ファイル、Editor 限定、ZIP 内容を検証する。
2. リリース対象コミットのタグ push、または手動起動でタグを指定する。
3. タグと manifest の一致を検証し、配布対象だけを ZIP 化する。
4. ZIP と package.json を GitHub Release のアセットに添付する。
5. 既存 Release の同名アセットは上書きせず、不一致なら失敗させる。
6. 自動化トークンの権限は必要なジョブに限り contents: write を付与する。

## 6. 共通 Listing
- 公開 URL: `https://rinya-mitsuki.github.io/vpm-repository/index.json`。
- source.json に対象 GitHub リポジトリを明示する。
- 全 Release をページ送りして取得し、draft と運用対象外の版を除外する。
- ZIP 内 manifest と公開 manifest を照合し、取得した ZIP の SHA-256 を Listing の zipSHA256 に記録する。package.json 自体にはハッシュを入れない。
- 同一 package ID / version の競合、ダウンロード失敗、manifest 不一致は公開を止める。
- 構造: packages → package ID → versions → version → manifest。
- 過去の公開 Listing と比較し、意図しない旧版消失を検出する。
- 完成した一覧を GitHub Pages にまとめて配置する。

## 7. Listing 更新 Actions
source.json の main への push、workflow_dispatch、定期 schedule を起点とする。まず公開 Release を読み取る定期更新方式を採用し、リポジトリ横断の書き込み用 PAT を必須にしない。定期実行には遅延があり、リリース直後の即時反映が必要なら Listing の手動実行を行う。後で即時通知を追加する場合は対象を限定した GitHub App 等を使用する。

取得・検証と Pages 配置を別ジョブにする。配置ジョブのみ pages: write / id-token: write を使用する。並行配置を制御し、不完全な一覧は公開しない。外部 Actions は検証したコミット SHA に固定する。

## 8. 既存 Assets 配布からの移行
元ソースの配置と GUID を確認するまで legacyFolders / legacyFiles は追加しない。これらは利用者のファイルを削除し得るため、ツール専用の範囲に限定する。Mitsuboshi_Studio 全体の共有フォルダーを削除対象にしない。既存ライセンスと第三者表記を維持する。

## 9. 完了条件
- GitHub Actions が成功し、Release の ZIP を認証なしで取得できる。
- 公開 index.json が取得でき、ZIP URL と SHA-256 が一致する。
- VCC に共通 URL を登録し、テストプロジェクトへ導入できる。
- Unity のコンパイル、起動、リネームと GUID 保持を確認する。v7 は通常の Undo に非対応であり、その仕様を維持する。
- 次の試験版へ VCC で更新し、重複コードや GUID 衝突がないことを確認する。
- 試験版を使って検証し、確認のためだけの安定版を発行しない。

## 10. 参照した公式仕様
- https://vcc.docs.vrchat.com/vpm/packages/
- https://vcc.docs.vrchat.com/vpm/repos/
- https://vcc.docs.vrchat.com/guides/create-listing/

## 初回移行の決定事項
- パッケージ版は 1.0.0-beta.1。従来の v7 とは別の番号体系。
- MIT License、著作権表示 Mitsuboshi_Studio（利用者指定）。
- ソースは UnityPowerRenameWindow_v7.cs のバイト列をそのまま保存。provenance.json に SHA-256 を記録。
- 旧 namespace Rinya.AssetTools を保持。パッケージ内ファイル名は UnityPowerRenameWindow.cs に固定。
- 元フォルダーに .meta がないため新しい GUID を一度だけ生成。以後保持する。
- 旧版はプロジェクト外へ手動退避。共有 Editor フォルダーを自動削除しない。
- 単体スクリプトを別途配布する場合は従来どおり末尾に改訂番号を付ける。
- README に個人用ツールの現状提供、サポート非保証、苦情は受け付けない旨を記載。

## 日常の更新手順
1. パッケージコードを修正する。
2. package.json の version と url 内の版を同時に変更する。CHANGELOG に変更点を追記。
3. パッケージ検証と必要な Unity テストを行い、main へ反映。
4. Release VPM package を main で手動実行、または v{version} タグを push。
5. 共通 Listing は毎時17分（UTC）の Actions で更新する。GitHub側の遅延、公開repoの60日非活動による schedule 停止に注意。必要なら Build VPM listing を手動実行する。
6. VCC で一覧を更新して対象プロジェクトに適用。beta の表示には Show Pre-Release Packages が必要。

## 次のツールを追加
新規リポジトリで同じ Packages/{package-id} 構成、manifest、Editor assembly、永続 .meta、LICENSE、README、CHANGELOG を用意する。package.py と release.py、workflow を共通雛形としてコピーし、パッケージ ID とリポジトリ名を置換する。テストの固定パス・期待値も対象に合わせる。最初の Release が公開できてから共通 source.json の githubRepos に owner/repository を追加する。

## 自動化の検証範囲
Python の単体テストは ZIP 再現性、SemVer、manifest の位置・整合、パストラバーサル、欠落アセット、既存版の削除・変異、Release API のページ送りを検証する。Unity の GUI / AssetDatabase の実行はこれらのテストに含まれない。

-- ==========================================
-- 7. 動作確認用サンプルクエリ
-- ==========================================

-- 1. テスト用ユーザーIDを確認 (Authentication > Users からUUIDをコピー)
-- 例: 'user-uuid-abc-123'

-- 2. テスト用テナントと所属を作成 (ダッシュボードから手動挿入するか、以下のSQLで)
-- insert into tenants (id, name) values ('tenant-uuid-001', 'Test Company A');
-- insert into organization_members (user_id, tenant_id) values ('user-uuid-abc-123', 'tenant-uuid-001');

-- 3. ユーザーになりすましてProductsをSelectしてみる
--    (これを実行すると、このトランザクション内だけ指定ユーザーの権限になります)
-- set local role authenticated;
-- set local "request.jwt.claim.sub" to 'user-uuid-abc-123'; -- ユーザーUUIDをセット

-- 所属テナントのデータ → 見えるはず
-- select * from products where tenant_id = 'tenant-uuid-001';

-- 所属していないテナント(適当なID)のデータ → 空の結果が返るはず
-- select * from products where tenant_id = 'tenant-uuid-999';

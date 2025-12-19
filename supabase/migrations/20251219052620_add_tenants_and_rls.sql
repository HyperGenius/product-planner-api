-- ==========================================
-- 3. Row Level Security (RLS) の有効化
-- ==========================================
-- 全テーブルでRLSを有効化（これで明示的な許可ポリシーがない限りアクセス不可になる）
alter table tenants enable row level security;
alter table organization_members enable row level security;
alter table equipment_groups enable row level security;
alter table equipments enable row level security;
alter table equipment_group_members enable row level security;
alter table products enable row level security;
alter table process_routings enable row level security;
alter table orders enable row level security;
alter table production_schedules enable row level security;


-- ==========================================
-- 4. RLSポリシーの定義
-- ==========================================
-- 現在のユーザー(auth.uid())が、指定されたテナントのメンバーかどうかを判定する関数
-- SECURITY DEFINER: この関数は作成者(postgres)の権限で実行されるため、RLSをバイパスしてorganization_membersをチェックできる
create or replace function is_tenant_member(_tenant_id uuid)
returns boolean as $$
begin
  return exists (
    select 1
    from organization_members
    where tenant_id = _tenant_id
      and user_id = auth.uid()
  );
end;
$$ language plpgsql security definer;


-- ==========================================
-- 5. 各テーブルのRLSポリシー設定
-- ==========================================

-- 5.1 tenants テーブル
-- 参照: 自分が所属しているテナントのみ見える
create policy "Users can view tenants they belong to"
  on tenants for select
  using ( is_tenant_member(id) );

-- ※ テナントの作成(Insert)は、通常サインアップフローのFunction経由で行うため
--   ここでは一旦ポリシーを定義せず、デフォルトで拒否(Deny All)の状態にしておきます。


-- 5.2 organization_members テーブル
-- ==========================
-- 参照: 自分の所属情報、または同じテナントのメンバー情報が見える
create policy "Users can view members in their tenants"
  on organization_members for select
  using (
    -- 自分自身のレコード
    user_id = auth.uid() 
    or
    -- 自分が所属するテナントの他のメンバー
    exists (
      select 1 from organization_members as om
      where om.tenant_id = organization_members.tenant_id
      and om.user_id = auth.uid()
    )
  );

-- ※ メンバー追加などは管理者機能になるため、ここではSelectのみ許可します。



-- ==========================================
-- 6. 各マスタ・業務テーブルへの共通ポリシー適用
-- ==========================================

-- 対象テーブルのリスト
-- equipment_groups, equipments, equipment_group_members, 
-- products, process_routings, orders, production_schedules

-- 6.1 Equipment Groups
create policy "Tenant isolation for equipment_groups"
  on equipment_groups
  for all -- Select, Insert, Update, Delete すべて
  using ( is_tenant_member(tenant_id) )
  with check ( is_tenant_member(tenant_id) );

-- 6.2 Equipments
create policy "Tenant isolation for equipments"
  on equipments
  for all
  using ( is_tenant_member(tenant_id) )
  with check ( is_tenant_member(tenant_id) );

-- 6.3 Equipment Group Members
create policy "Tenant isolation for equipment_group_members"
  on equipment_group_members
  for all
  using ( is_tenant_member(tenant_id) )
  with check ( is_tenant_member(tenant_id) );

-- 6.4 Products
create policy "Tenant isolation for products"
  on products
  for all
  using ( is_tenant_member(tenant_id) )
  with check ( is_tenant_member(tenant_id) );

-- 6.5 Process Routings
create policy "Tenant isolation for process_routings"
  on process_routings
  for all
  using ( is_tenant_member(tenant_id) )
  with check ( is_tenant_member(tenant_id) );

-- 6.6 Orders
create policy "Tenant isolation for orders"
  on orders
  for all
  using ( is_tenant_member(tenant_id) )
  with check ( is_tenant_member(tenant_id) );

-- 6.7 Production Schedules
create policy "Tenant isolation for production_schedules"
  on production_schedules
  for all
  using ( is_tenant_member(tenant_id) )
  with check ( is_tenant_member(tenant_id) );

# SUIJI Reddit 运营系统迁移说明 v0.1

建立日期：2026-05-22

## 迁移结论

当前系统可以比较方便地迁移，但还不是严格意义上的飞书“一键复制到另一个账号”。原因是飞书文档、表格、文件夹 token 和授权都绑定当前飞书账号/租户；换账号后需要重新导入文件并更新链接。

## 源文件位置

本地源文件：

- `Reddit运营中文手册-基于Masters-in-Marketing.md`
- `Reddit运营中文手册-基于Masters-in-Marketing.docx`
- `SUIJI_Reddit运营知识库_v0.1/SUIJI_Reddit运营知识库_v0.1.xlsx`
- `SUIJI_Reddit高赞内容结构库_v0.1/SUIJI_Reddit高赞内容结构库_v0.1.xlsx`
- `SUIJI_Reddit运营系统_v0.1/SUIJI_Reddit团队运营SOP_v0.1.docx`
- `SUIJI_Reddit运营系统_v0.1/SUIJI_Reddit运营工作台_v0.1.xlsx`

GitHub 存档：

- https://github.com/YueWangucsd/Suiji-repo-Skill

## 迁移到另一个飞书账号的步骤

1. 在新飞书账号里新建文件夹，例如 `SUIJI Reddit 运营系统 v0.1`。
2. 上传或导入 `SUIJI_Reddit团队运营SOP_v0.1.docx`，作为飞书文档使用。
3. 上传或导入 `SUIJI_Reddit运营工作台_v0.1.xlsx`，作为飞书表格使用。
4. 上传或导入 `SUIJI_Reddit运营知识库_v0.1.xlsx`，作为飞书表格使用。
5. 上传或导入 `SUIJI_Reddit高赞内容结构库_v0.1.xlsx`，作为飞书表格使用。
6. 上传或导入 `Reddit运营中文手册-基于Masters-in-Marketing.docx`，作为飞书文档使用。
7. 在新账号中重新生成索引文档，并替换所有旧飞书链接。
8. 如果要继续让 Codex 自动写入飞书，需要在新账号重新配置 lark-cli/lark-codex 授权、文档上传 scope 和目标文件夹权限。

## 迁移后需要重建的内容

- 飞书文件夹 token。
- 飞书文档和表格链接。
- lark-cli/lark-codex 授权。
- 自动化产出的目标文件夹。
- 团队成员权限。

## 不需要重建的内容

- SOP 内容。
- 工作台字段结构。
- KPI 定义。
- 知识库表结构。
- 高赞内容结构库表结构。
- reddit-jewelry-research skill 的 GitHub 存档。

## 当前注意事项

团队版 SOP 的 DOCX 已成功导入当前飞书账号，当前最新版链接为：https://f0ldzvcs4a2.feishu.cn/docx/Vus3dWGKRoc2PpxgY96c451Hn2g

当前飞书原生文件链接清单：https://f0ldzvcs4a2.feishu.cn/docx/GV08d0b9OoiBauxVws8c1vZEnmb

Subreddit 社区运营手册完整规则版：https://f0ldzvcs4a2.feishu.cn/docx/FJRPdggqwoAwYLxqSoScWjAvndf

迁移到其他飞书账号时，这个链接不能直接复用为目标账号文件；仍需在目标账号中重新导入 DOCX 并替换索引链接。

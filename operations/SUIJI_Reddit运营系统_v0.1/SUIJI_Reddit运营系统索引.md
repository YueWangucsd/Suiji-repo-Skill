# SUIJI Reddit 运营系统 v0.1

建立日期：2026-05-22  
当前阶段：0 到 1 前期准备 + 轻量试运营  
主目标：30% 客户痛点理解，70% 种子用户孵化

## 这个系统解决什么问题

SUIJI 现在已经有 Reddit 相关资料、社区库、首饰知识库、高赞内容结构库和自动化 research skill。问题不是缺信息，而是团队每天不知道该看什么、谁来做、怎么评论、怎么记录、怎么复盘。

这个系统把所有 Reddit 工作拆成三层：

1. 知识层：已经存在的首饰知识、社区库、高赞结构、Reddit Do's and Don'ts。
2. 运营层：每天给团队的优先队列、打卡表、专家任务、种子用户 CRM。
3. 研究层：每周固定产出的 Reddit insight report，继续沉淀痛点、社区变化、内容结构和产品机会。

## 文件清单

- `SUIJI_Reddit运营SOP_v0.1.md`  
  团队执行手册。定义目标、分工、每日流程、评论规则、风险边界、KPI 和复盘方式。

- `SUIJI_Reddit每日运营制度_v0.1.md`  
  每日团队工作流。说明每天如何使用 rising/new、如何打卡、专家怎么介入、哪些动作不能做。

- `SUIJI_Reddit周报制度_v0.1.md`  
  每周 research 报告的形式。保留研究能力，但把周报变成“战略洞察 + 下周运营输入”。

- `SUIJI_Reddit_skill修改方案_v0.1.md`  
  对 `reddit-jewelry-research` skill 的修改方案和落地口径。

- `SUIJI_Reddit运营工作台_v0.1.xlsx`  
  团队每日使用的表格模板。包含每日队列、团队打卡、专家任务、种子用户 CRM、周报输入、KPI 等。

## 和旧知识库的关系

旧知识库不废弃，分工如下：

- `Reddit运营中文手册`：合规和行为红线。
- `SUIJI_Reddit运营知识库_v0.1`：品牌边界、首饰知识、社区库、专家输入区。
- `SUIJI_Reddit高赞内容结构库_v0.1`：高赞帖子/评论结构、可复用表达骨架。
- `SUIJI_Reddit运营系统_v0.1`：团队每天执行和每周复盘的控制台。

## 每天怎么用

1. Codex/skill 生成 `每日运营打卡` 或更新工作台。
2. 团队先看 `今日优先队列`，优先处理低风险 rising。
3. 非专家成员做真实社区参与，不做产品硬推。
4. 首饰专家处理 `专家任务` 中的材料、结构、舒适度、搭配问题。
5. 每个人在 `团队打卡` 填写当天动作和发现。
6. 有价值用户进入 `种子用户CRM`。
7. 新痛点、新知识、新评论结构回写到对应知识库。

## 每周怎么用

每周继续产出 research 报告，但报告不再只是“本周看到什么”，而是输出：

- 客户痛点趋势
- 高价值社区变化
- 高互动内容结构
- 专家知识补充
- 种子用户候选
- 下周团队运营优先级
- 需要进入知识库的新内容

## 合规底线

Reddit 官方反垃圾政策强调不要进行重复或未经请求的大规模互动；Reddit 开发者文档也要求用户动作必须由用户明确触发，且应用不能投票。Reddit Pro organic playbook 建议企业先听、再评论，像社区成员一样提供价值，而不是直接营销。

因此本系统只自动化“听、筛、总结、排队、起草、记录”，不自动化发帖、评论、投票、私信或建号。

参考：

- Reddit Help: Spam — https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam
- Reddit Developers: User Actions — https://developers.reddit.com/docs/capabilities/server/userActions
- Reddit Pro Organic Playbook — https://redditinc.com/hubfs/Reddit%20Inc/Content/Reddit%20Pros%20organic%20playbook.pdf

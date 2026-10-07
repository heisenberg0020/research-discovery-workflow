# 同轮接续的决定性来源与阅读深度

2026-10-07。旧来源记录与科学稿不改；本补充区分原执行器深度、接续本人复核、定向协作者复核和未来验证。没有新科学观测，没有用来源重合增加证据数。原阶段实际检索为2026-10-06；本次定向公开资源/原件复读截止2026-10-07。

## 本人决定性复读

1. Dronavajjala，When Is Conformal Coverage Free?，COPA2026/PMLR329，当前根已保存28页PDF；接续用已有解析脚本静态读取pp3–5、9–18。Thm3 exact κ、Prop4非TU边界、Thm5–6 stationarity/Gaussian/independence及variance条件、§5任务/参数/测量已复核；原执行器此前全读28页。不是本轮重复实验。[原始记录](https://proceedings.mlr.press/v329/dronavajjala26a.html)。官方core/free_coverage的原blob检查仅沿用本轮记录，接续未重读或运行这两个文件；保留时序问题的局部范围与不推翻全部数值的限制。

2. Patel/Rayan/Tewari，Conformal Contextual Robust Optimization，AISTATS2024/PMLR238，当前根19页作者PDF；接续本人重读pp2–8及13。重构§3 min-distance score、union优化、K选择需不同校准/volume资料；§4.2 weather-derived costs与continuous flow、App A/B关键条件。原Eq12 squared-L2与本有限V范数score区分；support(U)=support(conv U)为本轮纸面语义身份，不称新定理。没系统审训练实验附录或重现表。[作者原PDF](https://www.ambujtewari.com/research/patel24conformal.pdf)。

3. robbuffet固定公开commit 01275c768dacd0be16cf28c391da99813ca14ff7。本人完整静态读README、MIT License、scores.py、calibration.py；先web读取README成功，GitHub tree API在web报不可访问，再以同一公开API curl只读成功，不掩盖失败。GPCP取min-L2、UnionRegion接口、batch校准默认NumPy quantile可确认；不是已适配arrival-ledger或原CPO全实验认证。未读完region.py/decision.py，未运行/安装/初始化submodule或下载预训练模型。[固定版README](https://github.com/yashpatel5400/robbuffet/blob/01275c768dacd0be16cf28c391da99813ca14ff7/README.md)、[scores.py](https://github.com/yashpatel5400/robbuffet/blob/01275c768dacd0be16cf28c391da99813ca14ff7/robbuffet/scores.py)、[calibration.py](https://github.com/yashpatel5400/robbuffet/blob/01275c768dacd0be16cf28c391da99813ca14ff7/robbuffet/calibration.py)。

4. Caltrans [PeMS Data Source](https://dot.ca.gov/programs/traffic-operations/mpr/pems-source)：本人本次完整相关正文复读，支持archive/free申请、1–2工作日通常审批与PeMS14历史重处理，不能证明本候选档案已获得或保留真实发布vintage。[Data Transformation](https://cagov.github.io/caldata-mdsa-caltrans-pems/data/data-transform/)与[Detector Health](https://cagov.github.io/caldata-mdsa-caltrans-pems/data/detector-health/)本人完整相关正文/表复读，支持sample聚合、日mart、补齐、全天health及ramp不impute；不支持逐record公共available_at。

5. 官方dbt docs网页静态抓取可返回0文本，但浏览器能读到内容。本人新建后台官方docs tab（没有读用户旧browser/history），复读如下三页的Description、全部Columns、Code：

- [int_vds__station_config](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.int_vds__station_config)：SCD2有效起止与segment_start/end/length；Code的config_log与current config关联；有效时间与公开到达时间不能混用。
- [geo__current_stations](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.geo__current_stations)：具体方向/覆盖段/点geometry字段；Code去掉有效起止并仅留current；不能直接认证历史210day。
- [imputation__detector_imputed_agg_five_minutes](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.imputation__detector_imputed_agg_five_minutes)：sample_timestamp为五分钟起点，健康/imputation方法/版本相关字段存在；mart只取ML/HV过去4天；字段表无逐record available_at。LAST MODIFIED表元数据不是历史发布账本。

## 定向资源worker已读，本人未逐页复读的限定证据

worker是同轮已知情的资源核查，非新独立探索；完整读本根指令、Skill/comparison-plan后只读取指定当前科学稿和公开资料。它与本人来源重合不是第二份独立科学确认。没有写文件或下载数据行。

- clearinghouse [station_meta](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/source/source.caldata_mdsa_caltrans_pems.clearinghouse.station_meta)、[station_raw](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/source/source.caldata_mdsa_caltrans_pems.clearinghouse.station_raw)、[station_metrics_agg_five_minutes](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.int_performance__station_metrics_agg_five_minutes)：Description/全部Columns与指定关联；miles/mph、ID、观测/imputation与测量时刻字段路线明确，未取得候选期实际资料。
- [SHN linework](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/source/source.caldata_mdsa_caltrans_pems.geo_reference.shn_lines)与[nearby_stations](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.int_vds__nearby_stations)：Description/全部Columns及关联条件读完。前者2022-10-10 TSN抽取给方向几何/odometer，后者用于同freeway/direction/type的imputation，不能代替connector拓扑。
- [All Roads schema](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/chhighway/All_Roads/FeatureServer/0)与[ItemInfo](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/chhighway/All_Roads/FeatureServer/0/iteminfo)：完整schema/许可，CC BY4.0、不支持historic-moment、无完整性/及时性保证；SHN Odometer schema完整、Intersection只读说明和前段字段。没读实际图层行或构造路径。
- [Data Relay](https://cagov.github.io/caldata-mdsa-caltrans-pems/data/data-relay/)只读overview/组件/调度/指定字段，内部3h取数/6h上传不等于公共SLA；[Data Loading](https://cagov.github.io/caldata-mdsa-caltrans-pems/data-loading/)和[Incremental Models](https://cagov.github.io/caldata-mdsa-caltrans-pems/incremental/)全相关页读，新旧/可full-refresh条件只支持版本谨慎。不能由调度指定实际a_jr。
- [PeMS申请页](https://pems.dot.ca.gov/?dnode=apply)全页读，未填/提交；实时feed另需批准，web账号尚未获。公开[clearinghouse目录](https://pems.dot.ca.gov/feeds/clhouse/)仅目录元数据；没有进入数据文件。14.0 release PDF本次读取失败，未计已读。

## 比较审计与证据身份

第二位同轮比较worker只读Q5-R/coordinator-reading、完整Skill/comparison-plan并静态复读CPO pp2–8/13，未写文件/执行研究。它提出固定reference d、当前方向重投影历史、same-capacity B0+、D/R loss重复、box score零core及support凸包等纸面检查，已纳入Q7-A。本人的最终责任是复核操作与算术，不能把审计作为经验支持。

本次没有补完储备B的Marx全部oracle证明或最新行动条件机制，因此B保持partial。所有CPU、storage、样本数是给定假设下算术；未测实验吞吐、效果、power、实际变化频率或发布latency。主资源资格结论是已读公开说明不能证实四项所需证据，不是宣布资源不可能存在。

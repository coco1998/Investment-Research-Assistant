# 本地投研工作台

这个工作台复刻 Workbuddy 投研工作台的使用体验，但数据源改为通用 `workspace/`。

## 启动

```bash
python3 workbench/serve.py
```

## 刷新数据

```bash
python3 workbench/refresh_data.py
```

解析器会读取：

- `workspace/projects/*/master.md`
- `workspace/projects/*/reports/*.md`
- `workspace/projects/*/materials/**/*`
- `workspace/meetings/*.md`
- `workspace/knowledge/2_wiki/entities/*.md`
- `workspace/knowledge/2_wiki/concepts/*.md`

生成的 `workbench/data.js` 不建议提交到 Git。

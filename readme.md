## Staff Commands

```bash
$ flask staff create <username> <password> <department> <faculty>
```

```bash
$ flask staff delete
```

```bash
$ flask staff create_report
```

## Student Commands

```bash
$ flask student list
```

```bash
$ flask student get_report_by_id <id>
```

```bash
$ flask student update_student <student_id> [firstname] [lastname] [new_student_id]
```

```bash
$ flask student delete
```

```bash
$ flask student update_report <report_id> [review] [rating]
```

```bash
$ flask student delete_report <report_id>
```

```bash
$ flask student list_reports [order]
```

```bash
$ flask student search_by_id <student_id>
```

```bash
$ flask student search_by_name <firstname> <lastname>
```

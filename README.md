# notion-echome

This simple python script uses the [notion-sdk-py](https://github.com/ramnes/notion-sdk-py) client to update a [Notion](https://www.notion.so/) table with the latest Virtual Machines managed with [ecHome](https://github.com/mgtrrz/echome).

It's mostly an excuse to play with dataclasses so you can easily create a class with the table columns/fields:

```
@dataclass
class VmObject(TableRow):
    IP: str = field(metadata={'type':'title'})
    Name: str = field(default=None, metadata={'type':'rich_text'})
    Type: str = field(default=None, metadata={'type':'select'})
    Host: str = field(default=None, metadata={'type':'select'})
    Status: str = field(default=None, metadata={'type':'select'})
    Hostname: str = field(default=None, metadata={'type':'rich_text'})
    URL: str = field(default=None, metadata={'type':'rich_text'})
    Description: str = field(default=None, metadata={'type':'rich_text'})
```

Then you can define new objects or rows with:

```
newRow = VmObject(
    IP="127.0.0.1",
    Name="Example",
    Type="VM",
    Host="ecHome",
    status="Running,
    Description="Example description"
)
```

And simply pass it to the notion-client with `.render_json()`

```
notion.pages.create(
    parent={
        "database_id": echomeDb
    },
    properties=newRow.render_json()
)
```

See `main.py` for the full details.

### Requirements

* Python >3.9
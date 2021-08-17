import os
from notion_client import Client
from pprint import pprint
from dataclasses import dataclass, field
from echome import Session
import types

echomeDb = os.environ["NOTION_DB_ID"]
notion = Client(auth=os.environ["NOTION_TOKEN"])

dbs = notion.databases.query(database_id=echomeDb)
ips_in_table = {}
for result in dbs["results"]:
    pprint(result)
    ips_in_table[result["id"]] = result["properties"]["IP"]["title"][0]["plain_text"]

pprint(ips_in_table)

@dataclass
class TableRow:
    def _title(self, text) -> dict:
        return {
            "title": [{
                "text": {
                    "content": text
                }
            }]
        }
    
    def _rich_text(self, text) -> dict:
        return {
            "rich_text": [{
                "text": {
                    "content": text
                }
            }]
        }
    
    def _select(self, text) -> dict:
        return {
            "select": {
                "name": text
            }
        }
    
    def _get_vars(self) -> list:
        vars = []
        for var in dir(self):
            if not isinstance(getattr(self, var), \
                (types.FunctionType, types.BuiltinFunctionType)) and \
                not var.startswith("_") and var != "render_json":
                vars.append(var)
        return vars
    
    def render_json(self) -> dict:
        vars = self._get_vars()
        obj = {}
        for var in vars:
            if getattr(self, var) is not None:
                type = self.__dataclass_fields__[var].metadata['type']
                type = f"_{type}"
                obj[var] = getattr(self, type)(getattr(self, var))
        return obj

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

    def __str__(self) -> str:
        return self.IP


# Check echome for new VMs
vm_client = Session().client("Vm")
try:
    vms = vm_client.describe_all()
except Exception as e:
    print("Could not retrieve list of VMs!")
    print(e)
    exit(1)

for vm in vms:
    name = vm["tags"]["Name"] if "Name" in vm["tags"] else None
    ip = vm["attached_interfaces"]["config_at_launch"]["private_ip"]
    status = vm["state"]["state"]

    if ip not in ips_in_table.values():
        # add it to the Notion table
        newVm = VmObject(
            IP=ip,
            Name=name,
            Type="VM",
            Host="ecHome",
            Status=status,
            Description=vm["tags"]["Description"] if "Description" in vm["tags"] else None
        )
        pprint(newVm)

        notion.pages.create(
            parent={
                "database_id": echomeDb
            },
            properties=newVm.render_json()
        )

        #ips_in_table.remove(ip)
    
# Are there any IPs left over from the Notion table?
# If so, they're probably terminated VMs. Remove them!


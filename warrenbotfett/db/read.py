from datetime import datetime

from supabase import Client, create_client

from warrenbotfett.common import BotSummary
from warrenbotfett.utils.secrets import secrets

supabase: Client = create_client(secrets.supabase_url, secrets.supabase_key)


def read_summary() -> dict[datetime, BotSummary]:
    response = supabase.table("DailySummaries").select("*").execute()
    return {
        datetime.fromisoformat(d["created_at"]): BotSummary.model_validate_json(
            d["summary"]
        )
        for d in response.data
    }


def read_agent_results():
    response = supabase.table("agent_results").select("*").execute()
    return response.data
    # return {
    #     datetime.fromisoformat(d["created_at"]): BotSummary.model_validate_json(
    #         d["summary"]
    #     )
    #     for d in response.data
    # }


if __name__ == "__main__":
    # summary = read_summary()
    # print(f"{summary=}")
    data = read_agent_results()
    print(data)
    d = data[0]
    import json


    messages = json.loads(d["messages"])
    for m in messages:
        print(m["kind"])
    """
    data[0].keys()
    dict_keys(['id', 'created_at', 'messages', 'output', 'usage'])
    ['__args__', '__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__',
    '__getattr__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__'
     '__instancecheck__', '__iter__', '__le__', '__lt__', '__metadata__', '__module__', '__mro_entries__', '__ne__', '__new__', 
     '__or__', '__origin__', '__parameters__', '__reduce__', '__reduce_ex__', '__repr__', '__ror__', '__setattr__', 
     '__sizeof__', '__slots__', '__static_attributes__', '__str__', '__subclasscheck__', '__subclasshook__', '__weakref__', 
     '_determine_new_args', '_getitem', '_inst', '_make_substitution', '_name', 'copy_with']
    """

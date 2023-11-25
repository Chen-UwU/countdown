"""
@Description :   Definition of Event Class
@Author      :   XiaoYuan
@Time        :   2023/11/25 18:35:46
"""
from typing import Tuple,List
from dataclasses import dataclass
from datetime import datetime
import pickle
import os

base = os.path.abspath(os.path.dirname(__file__))
PKL_FILE = os.path.join(base,r"event\event.pkl")

if not os.path.isfile(PKL_FILE):
    with open(PKL_FILE, "wb") as f:
        pickle.dump([], f)


@dataclass
class Style:
    """Style for Countdown Event"""
    name:str
    pos:Tuple[int|float,int|float,int|float]
    size:int|float
    color:Tuple[int, int, int]|str
    font_path:str

    def __repr__(self) -> str:
        return f"< Style:{self.name} >"

    def __getitem__(self, key:str):
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(f"{self} has not {key}")

    def to_dict(self) -> dict:
        """把Style中必要的属性保存到字典中返回"""
        needed = ["pos", "size", "color", "font_path"]
        return dict(zip(needed,
                        [self[i] for i in needed]))

class StyleGroup:
    """由三个Style构成的StyleGroup，分别为Day,Hour,Minute设置Style"""
    def __init__(self,day:Style,hour:Style,minute:Style) -> None:
        self.day = day
        self.hour = hour
        self.minute = minute

    def __repr__(self) -> str:
        return f"< StyleGroup: {self.day}-{self.hour}-{self.minute} >"

    def __getitem__(self, key:str):
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(f"{self} has not {key}")

    def get_style(self) -> dict:
        """把StyleGroup中必要的属性保存到字典中返回"""
        needed = ["day", "hour", "minute"]
        return dict(zip(needed,
                        [self[i] for i in needed]))

class Event:
    """事件类"""
    def __init__(self, event:str, start:datetime, end:datetime, stlye:StyleGroup) -> None:
        self.event = event
        self.start = start
        self.end = end
        self.style = stlye

    def __repr__(self) -> str:
        return f"<Event:{self.event}>"

    def __eq__(self, other:"datetime|Event") -> bool:
        if isinstance(other, datetime):
            return other in (self.start, self.end)
        if isinstance(other, Event):
            return self.start == other.start and self.end == other.end
        raise TypeError(f"'==' can not be used between {type(other)} and Event")

    def __lt__(self, other:"datetime|Event") -> bool:
        if isinstance(other, datetime):
            return self.end < other
        if isinstance(other, Event):
            return self.end < other.start
        raise TypeError(f"'<' can not be used between {type(other)} and Event")

    def __gt__(self, other:"datetime|Event") -> bool:
        if isinstance(other, datetime):
            return self.start > other
        if isinstance(other, Event):
            return self.start > other.end
        raise TypeError(f"'>' can not be used between {type(other)} and Event")

    def __contains__(self, other:"datetime|Event") -> bool:
        if isinstance(other, datetime):
            return self.start <= other <= self.end
        if isinstance(other, Event):
            return self.start <= other.start and self.end >= other.end
        raise TypeError(f"'in' can not be used between {type(other)} and Event")

def empty_event():
    """清空事件"""
    with open(PKL_FILE, "wb") as f:
        pickle.dump([], f)

def load_event() -> List[Event]:
    """加载事件"""
    with open(PKL_FILE, "rb") as file:
        event_list = pickle.load(file)
    return event_list

def update_event(event_list:List[Event]):
    """更新事件"""
    with open(PKL_FILE, "wb") as file:
        pickle.dump(event_list, file)

def add_event(event:str, start:datetime, end:datetime, stlye:StyleGroup)->None:
    """添加新事件"""
    new_event = Event(event, start, end, stlye)
    event_list = load_event()
    event_list.append(new_event)
    update_event(event_list)

def del_event(event: str):
    """删除事件"""
    event_list = load_event()
    for ind, ele in enumerate(event_list):
        if ele.event == event:
            event_list = event_list[:ind] + event_list[ind+1:]
    update_event(event_list)



if __name__ == "__main__":
    style = Style("test", (0,0,0), 10, "red", r"font\AaLingJunTi-2.ttf")
    # print(style.to_dict())
    sg = StyleGroup(style,style,style)
    # print(sg.get_style())
    start1 = datetime(2023,10,1)
    end1 = datetime(2023,10,7)
    empty_event()
    add_event("国庆",start1,end1,sg)
    elist = load_event()
    print(elist)
    del_event("国庆")
    elist = load_event()
    print(elist)

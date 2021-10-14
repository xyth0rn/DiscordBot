# 檔名：todo_list.py
# 功能：TODO list (新增、刪除、顯示)
# TODO：刪除、顯示、排序、清空、儲存記錄至檔案 (HINT: file I/O, pickle)

import discord
from discord.ext import commands
import re
import os
import pandas as pd

# 一項 Todo 的 class
class Todo:
    # 初始化
    def __init__(self, date, label, item):
        # 判斷是否為合法的日期 (不是很完整的判斷)
        d = re.compile("[0-9]{1,2}/[0-9]{1,2}")
        assert d.match(date)
        self.date = date
        self.label = label
        self.item = item

    # 小於 < (定義兩個 Todo 之間的「小於」，sort 時會用到)
    def __lt__(self, other):
        if self.date[:2] < other.date[:2]:
            return self.date < other.date
        
        elif self.date[:2] == other.date[:2]:
            if self.date[3:] < other.date[3:]:
                return self.date < other.date

    # 等於 = (判斷兩個 Todo 是否相等)
    def __eq__(self, other):
        return self.date==other.date and self.label==other.label and self.item==other.item

    # 回傳一個代表這個 Todo 的 string
    def __repr__(self):
        return f"{self.date} {self.label} {self.item}"

# Todo list 相關 commands
class Todo_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todo_list = []
        
        todo_df = pd.read_csv(r'..\storage\todo.csv')
        for i in range(todo_df.shape[0]):
            r_date  = todo_df.loc[i][0]
            r_label = todo_df.loc[i][1]
            r_item  = todo_df.loc[i][2]

            self.todo_list.append( Todo(r_date, r_label, r_item) )
        
        # print(self.todo_list)


    # $add <date> <label> <item>
    @commands.command(
        help = '''
        Add a task in TODO list.
        $add <date> <label> <item>
            ex. $add 06/24 Sprout Discord Bot HW
        ''',
        brief = "Add a task in TODO list."
    )
    async def add(self, ctx, date=None, label=None, *, item=None):
        if date == None or label == None or item == None:
            return await ctx.send("Error: Invalid input.\nPlease enter <date> <label> <item>.")

        if date[:2].isdigit() == False or date[3:].isdigit() == False:
            return await ctx.send("Error: Invalid input.\nPlease enter <date> <label> <item>.")
        
        # 依照輸入建立一個 Todo object
        task = Todo(date, label, item)

        if int(date[0:2]) < 1 or int(date[0:2]) > 12:
            return await ctx.send("Error: Invalid month.")

        if int(date[3:]) < 1 or int(date[3:]) > 31:
            return await ctx.send("Error: Invalid day.")

        if ( task in self.todo_list ) == True:
            return await ctx.send('"{}" is already in TODO list.'.format(item))
        
        # 把 Todo 加進 list
        self.todo_list.append(task)
        # 按照日期排序，若實作了 Todo 的 __lt__ 則可以直接用 sort() 排序
        self.todo_list.sort()

        todo_df = pd.DataFrame(columns=['date', 'label', 'item'])
        for task in self.todo_list:
            row = [task.date, task.label, task.item]
            todo_df.loc[len(todo_df)] = row
        todo_df.to_csv(r'..\storage\todo.csv', index=False)

        # 印出加入成功的訊息
        # ( self.todo_list )
        return await ctx.send('"{}" is added to TODO list.'.format(item))


    # $done <date> <label> <item>
    @commands.command(
        help = '''
        Done a task in TODO list.
        $done <date> <label> <item>
            ex. $done 6/24 Sprout Discord Bot HW
        ''',
        brief = "Done a task in TODO list."
    )
    async def done(self, ctx, date=None, label=None, *, item=None): # * 代表 label 後面所有的字都會放到 item 內
        if date == None or label == None or item == None:
            return await ctx.send("Error: Invalid input.\nPlease enter <date> <label> <item>.")

        try:
            task = Todo(date, label, item)
        
        except Exception as e:
            print(e)
            return await ctx.send("Error: Invalid input.\nPlease enter <date> <label> <item>.")

        if (task in self.todo_list) == False:
            return await ctx.send("Error: Input item not found.")

        for i in range( len(self.todo_list) ):
            if self.todo_list[i] == task:
                self.todo_list.pop(i)
        
                todo_df = pd.DataFrame(columns=['date', 'label', 'item'])
                for task in self.todo_list:
                    row = [task.date, task.label, task.item]
                    todo_df.loc[len(todo_df)] = row
                todo_df.to_csv(r'..\storage\todo.csv', index=False)

                # print( self.todo_list )
                return await ctx.send( 'Hooray! You finished ' + str(item) +'.')


    # $show [label]
    @commands.command(
        help = '''
        Show all tasks with the label(if specified) sorted by date.
        $show
            ex. $show
        or
        $show <label>
            ex. $show Sprout
        ''',
        brief = "Show all TODO with the label if specified sorted by date." # 輸入 $help 時顯示
    )
    async def show(self, ctx, label=None):
        if label == None:
            for task in self.todo_list:
                await ctx.send( task )

        else:
            cnt = 0
            for task in self.todo_list:
                if task.label == label:
                    cnt += 1
                    await ctx.send( task )
            if cnt == 0:
                await ctx.send('{} is not in TODO List.'.format(label))
        
        return


    # $clear
    @commands.command(help = "Clear TODO list.", brief = "Clear TODO list.")
    async def clear(self, ctx):
        try:
            self.todo_list = []

            todo_df = pd.DataFrame(columns=['date', 'label', 'item'])
            todo_df.to_csv(r'..\storage\todo.csv', index=False)

            # print(self.todo_list)
            return await ctx.send("TODO list is cleared.")
        
        except Exception as e:
            print(e)
            return await ctx.send("Error: Invalid input.")


def setup(bot):
    bot.add_cog(Todo_list(bot))

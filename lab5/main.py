import tkinter as tk
from tkinter import messagebox, ttk,filedialog
import mysql.connector
from datetime import datetime
import csv

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("图书管理系统")
        self.root.geometry("800x600")
        self.db_config = {
            'host': 'localhost',
            'user': 'user',
            'password': 'password',
            'database': 'librarydb',
            'buffered': True
        }
        self.is_logged_in = False
        self.create_login_window()

    def get_db_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("错误", f"数据库连接失败: {err}")
            return None
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# =============================== handle the start page =======================================
    def create_login_window(self):
        self.clear_window()
        tk.Button(self.root, text="管理员登录", command=self.show_login_page,width=100,height=5).pack(pady=10)
        tk.Button(self.root, text="图书查询", command=self.show_query_window,width=100,height=5).pack(pady=10)


# =============================== handle the logic of login =======================================

    def show_login_page(self):
        self.clear_window()
        tk.Label(self.root, text="管理员登录", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="用户ID:").pack()
        self.user_id_entry = tk.Entry(self.root)
        self.user_id_entry.pack()
        tk.Label(self.root, text="密码:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        tk.Button(self.root, text="登录", command=self.login).pack(pady=10)
        tk.Button(self.root, text="返回主页面", command=self.create_login_window).pack(pady=10)

    def login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Users WHERE UserID = %s AND Password = %s", (user_id, password))
                if cursor.fetchone():
                    messagebox.showinfo("成功", "登录成功！")
                    self.is_logged_in = True
                    self.show_main_menu()
                else:
                    messagebox.showerror("错误", "用户ID或密码错误")
                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"登录失败: {err}")
            finally:
                conn.close()

# =============================== main menu =======================================
    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="图书管理系统 - 主菜单", font=("Arial", 16)).pack(pady=20)
        buttons = [
            ("图书入库", self.show_book_entry_window),
            ("图书查询", self.show_query_window),
            ("借书管理", self.show_borrow_window),
            ("还书管理", self.show_return_window),
            ("借书证管理", self.show_card_management_window),
            ("登出", self.create_login_window)
        ]
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command, width=100,height=5).pack(pady=5)

# =============================== handle the logic of query of the book =======================================

    def show_query_window(self):
        self.clear_window()
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        condition_frame = tk.LabelFrame(main_frame, text="查询条件", font=("Arial", 12))
        condition_frame.pack(fill="x", pady=10)

        tk.Label(condition_frame, text="书号:").grid(row=0, column=0, padx=5, sticky="e")
        self.book_no_entry = tk.Entry(condition_frame, width=15)
        self.book_no_entry.grid(row=0, column=1, padx=5, sticky="w")

        tk.Label(condition_frame, text="书名:").grid(row=0, column=2, padx=5, sticky="e")
        self.book_name_entry = tk.Entry(condition_frame, width=20)
        self.book_name_entry.grid(row=0, column=3, padx=5, sticky="w")

        tk.Label(condition_frame, text="类别:").grid(row=0, column=4, padx=5, sticky="e")
        self.category_entry = tk.Entry(condition_frame, width=15)
        self.category_entry.grid(row=0, column=5, padx=5, sticky="w")

        tk.Label(condition_frame, text="作者:").grid(row=1, column=0, padx=5, sticky="e")
        self.author_entry = tk.Entry(condition_frame, width=15)
        self.author_entry.grid(row=1, column=1, padx=5, sticky="w")

        tk.Label(condition_frame, text="出版社:").grid(row=1, column=2, padx=5, sticky="e")
        self.publisher_entry = tk.Entry(condition_frame, width=20)
        self.publisher_entry.grid(row=1, column=3, padx=5, sticky="w")

        range_frame = tk.Frame(condition_frame)
        range_frame.grid(row=2, column=0, columnspan=6, pady=10)

        tk.Label(range_frame, text="出版年份范围:").pack(side="left", padx=5)
        self.min_year_entry = tk.Entry(range_frame, width=8)
        self.min_year_entry.pack(side="left", padx=2)
        tk.Label(range_frame, text="-").pack(side="left")
        self.max_year_entry = tk.Entry(range_frame, width=8)
        self.max_year_entry.pack(side="left", padx=2)

        tk.Label(range_frame, text="价格范围:").pack(side="left", padx=10)
        self.min_price_entry = tk.Entry(range_frame, width=8)
        self.min_price_entry.pack(side="left", padx=2)
        tk.Label(range_frame, text="-").pack(side="left")
        self.max_price_entry = tk.Entry(range_frame, width=8)
        self.max_price_entry.pack(side="left", padx=2)

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="查询", command=self.query_books, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="重置条件", command=self.clear_query_conditions, width=12).pack(side="left", padx=5)
        tk.Button(main_frame, text="返回主菜单", command=self.create_login_window if not self.is_logged_in else self.show_main_menu).pack(pady=5)

        self.tree = ttk.Treeview(main_frame, columns=("书号", "书名", "类别", "作者", "出版社", "年份", "价格", "库存"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def clear_query_conditions(self):
        self.book_no_entry.delete(0, tk.END)
        self.book_name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.publisher_entry.delete(0, tk.END)
        self.min_year_entry.delete(0, tk.END)
        self.max_year_entry.delete(0, tk.END)
        self.min_price_entry.delete(0, tk.END)
        self.max_price_entry.delete(0, tk.END)

    def query_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conditions = []
        params = []

        exact_fields = {
            "BookNo": self.book_no_entry.get().strip(),
            "BookName": self.book_name_entry.get().strip(),
            "BookType": self.category_entry.get().strip(),
            "Author": self.author_entry.get().strip(),
            "Publisher": self.publisher_entry.get().strip()
        }

        for field, value in exact_fields.items():
            if value:
                conditions.append(f"{field} LIKE %s")
                params.append(f"%{value}%")

        try:
            min_year = self.min_year_entry.get().strip()
            max_year = self.max_year_entry.get().strip()
            if min_year:
                conditions.append("Year >= %s")
                params.append(int(min_year))
            if max_year:
                conditions.append("Year <= %s")
                params.append(int(max_year))

            min_price = self.min_price_entry.get().strip()
            max_price = self.max_price_entry.get().strip()
            if min_price:
                conditions.append("Price >= %s")
                params.append(float(min_price))
            if max_price:
                conditions.append("Price <= %s")
                params.append(float(max_price))
        except ValueError:
            messagebox.showerror("输入错误", "年份和价格必须为有效数字")
            return

        query = "SELECT BookNo, BookName, BookType, Author, Publisher, Year, Price, Storage FROM Books"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY BookNo ASC"

        try:
            conn = self.get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                for row in cursor.fetchall():
                    self.tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("数据库错误", f"查询失败: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

# =============================== handle the logic of borrowing books =======================================
    def show_borrow_window(self):
        self.clear_window()
        tk.Label(self.root, text="借书管理", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="借书证卡号:").pack()
        self.card_no_borrow = tk.Entry(self.root)
        self.card_no_borrow.pack()
        tk.Label(self.root, text="书号:").pack()
        self.book_no_borrow = tk.Entry(self.root)
        self.book_no_borrow.pack()
        tk.Button(self.root, text="借书", command=self.borrow_book).pack(pady=10)
        tk.Button(self.root, text="返回主菜单", command=self.show_main_menu).pack(pady=5)

    def borrow_book(self):
        card_no = self.card_no_borrow.get()
        book_no = self.book_no_borrow.get()
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM LibraryCard WHERE CardNo = %s", (card_no,))
                if cursor.fetchone():
                    is_card_exist = True
                else:
                    is_card_exist = False
                if not is_card_exist:
                    messagebox.showerror("错误", "借书证卡号不存在")
                    return
                else:
                    cursor.execute("SELECT Storage FROM Books WHERE BookNo = %s", (book_no,))
                    result = cursor.fetchone()
                    if result and result[0] > 0:
                        cursor.execute(
                            "INSERT INTO LibraryRecords (CardNo, BookNo, LentDate, Operator) VALUES (%s, %s, %s, %s)",
                            (card_no, book_no, datetime.now(), "admin")
                        )
                        cursor.execute("UPDATE Books SET Storage = Storage - 1 WHERE BookNo = %s", (book_no,))
                        conn.commit()
                        messagebox.showinfo("成功", "借书成功")
                    elif not result:
                        messagebox.showerror("错误","未找到该书号的图书")
                    else:
                        messagebox.showerror("错误", "图书无库存")
                    cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"借书失败: {err}")
            finally:
                conn.close()

    def show_return_window(self):
        self.clear_window()
        tk.Label(self.root, text="还书管理", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="借书证卡号:").pack()
        self.card_no_return = tk.Entry(self.root)
        self.card_no_return.pack()
        tk.Label(self.root, text="书号:").pack()
        self.book_no_return = tk.Entry(self.root)
        self.book_no_return.pack()
        tk.Button(self.root, text="还书", command=self.return_book).pack(pady=10)
        tk.Button(self.root, text="返回主菜单", command=self.show_main_menu).pack(pady=5)

    def return_book(self):
        card_no = self.card_no_return.get()
        book_no = self.book_no_return.get()
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT FID FROM LibraryRecords WHERE CardNo = %s AND BookNo = %s AND ReturnDate IS NULL",
                    (card_no, book_no)
                )
                result = cursor.fetchone()
                if result:
                    cursor.execute("UPDATE LibraryRecords SET ReturnDate = %s WHERE FID = %s", (datetime.now(), result[0]))
                    cursor.execute("UPDATE Books SET Storage = Storage + 1 WHERE BookNo = %s", (book_no,))
                    conn.commit()
                    messagebox.showinfo("成功", "还书成功")
                else:
                    messagebox.showerror("错误", "未找到该卡号的借书记录")
                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"还书失败: {err}")
            finally:
                conn.close()

# =============================== handle the logic of cards' addition or deletion =======================================

    def show_card_management_window(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(main_frame, text="借书证管理", font=("Arial", 16)).grid(row=0, column=0, columnspan=5, pady=10)

        # show all cards
        self.tree = ttk.Treeview(main_frame, columns=("卡号", "姓名", "单位", "类别", "更新时间"), show="headings", height=8)
        for col in ["卡号", "姓名", "单位", "类别", "更新时间"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=5, pady=10, sticky="nsew")

        # add new card
        add_frame = tk.LabelFrame(main_frame, text="添加新借书证", font=("Arial", 10))
        add_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="ew")
        
        self.add_entries = {}
        add_fields = ["卡号", "姓名", "单位", "类别"]
        for i, field in enumerate(add_fields):
            tk.Label(add_frame, text=f"{field}:").grid(row=0, column=i, padx=5)
            entry = tk.Entry(add_frame, width=18)
            entry.grid(row=1, column=i, padx=5)
            self.add_entries[field] = entry
        
        tk.Button(add_frame, text="添加", command=self.add_card, width=10).grid(row=1, column=4, padx=10)

        # delete card
        del_frame = tk.LabelFrame(main_frame, text="删除借书证", font=("Arial", 10))
        del_frame.grid(row=3, column=0, columnspan=5, pady=10, sticky="ew")
        
        tk.Label(del_frame, text="输入卡号:").grid(row=0, column=0, padx=5)
        self.del_entry = tk.Entry(del_frame, width=25)
        self.del_entry.grid(row=0, column=1, padx=5, sticky="w")
        tk.Button(del_frame, text="删除", command=self.delete_card, width=10).grid(row=0, column=4, padx=10)

        # return
        tk.Button(main_frame, text="返回主菜单", command=self.show_main_menu, width=15).grid(row=4, column=4, pady=20)

        self.refresh_card_list()

        main_frame.grid_columnconfigure(4, weight=1)  
        main_frame.grid_rowconfigure(1, weight=1)     

    def refresh_card_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT CardNo, Name, Department, CardType, UpdateTime FROM LibraryCard ORDER BY CardNo ASC")
                for row in cursor.fetchall():
                    self.tree.insert("", "end", values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"加载数据失败: {err}")
            finally:
                cursor.close()
                conn.close()

    def add_card(self):
        data = {field: entry.get() for field, entry in self.add_entries.items()}
        
        if any(value.strip() == "" for value in data.values()):
            messagebox.showwarning("输入错误", "所有字段必须填写")
            return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # is the card valid?
                cursor.execute("SELECT CardNo FROM LibraryCard WHERE CardNo = %s", (data["卡号"],))
                if cursor.fetchone():
                    messagebox.showerror("错误", "该卡号已存在")
                    return
                
                # insert
                query = """INSERT INTO LibraryCard (CardNo, Name, Department, CardType, UpdateTime)
                        VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (
                    data["卡号"], 
                    data["姓名"], 
                    data["单位"], 
                    data["类别"], 
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                
                for entry in self.add_entries.values():
                    entry.delete(0, tk.END)
                self.refresh_card_list()
                messagebox.showinfo("成功", "借书证添加成功")
                
            except mysql.connector.Error as err:
                messagebox.showerror("数据库错误", f"添加失败: {err}")
            finally:
                cursor.close()
                conn.close()

    def delete_card(self):
        card_no = self.del_entry.get().strip()
        
        if not card_no:
            messagebox.showwarning("输入错误", "请输入要删除的卡号")
            return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # exist?
                cursor.execute("SELECT * FROM LibraryCard WHERE CardNo = %s", (card_no,))
                if not cursor.fetchone():
                    messagebox.showerror("错误", "未找到该借书证")
                    return
                
                # confirm to delete
                # think twice is it.
                if messagebox.askyesno("确认删除", f"确定要删除卡号 {card_no} 吗？"):
                    cursor.execute("DELETE FROM LibraryCard WHERE CardNo = %s", (card_no,))
                    conn.commit()
                    
                    self.del_entry.delete(0, tk.END)
                    self.refresh_card_list()
                    messagebox.showinfo("成功", "借书证已删除")
                    
            except mysql.connector.Error as err:
                messagebox.showerror("数据库错误", f"删除失败: {err}")
            finally:
                cursor.close()
                conn.close()


# =============================== handle the logic of add books into the database =======================================
    def show_book_entry_window(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(main_frame, text="图书入库管理", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)


        self.tree = ttk.Treeview(main_frame, 
                            columns=("书号", "书名", "类别", "作者", "出版社", "年份", "价格", "库存"),
                            show="headings",
                            height=10)
        columns_settings = [
            ("书号", 100), ("书名", 150), ("类别", 80), 
            ("作者", 100), ("出版社", 120), ("年份", 80),
            ("价格", 80), ("库存", 80)
        ]
        for col, width in columns_settings:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=4, pady=10, sticky="nsew")

        entry_frame = tk.LabelFrame(main_frame, text="入库操作", font=("Arial", 10))
        entry_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

        fields_group1 = [
            ("书号", "book_no", 18),
            ("书名", "book_name", 25),
            ("类别", "category", 15)
        ]
        
        fields_group2 = [
            ("作者", "author", 20),
            ("出版社", "publisher", 20),
            ("出版年份", "year", 10)
        ]
        
        fields_group3 = [
            ("价格", "price", 10),
            ("入库数量", "quantity", 10)
        ]

        self.entries = {}
        
        for col, (label, field, width) in enumerate(fields_group1):
            tk.Label(entry_frame, text=label+":").grid(row=0, column=col*2, padx=5, sticky="e")
            entry = tk.Entry(entry_frame, width=width)
            entry.grid(row=0, column=col*2+1, padx=5, sticky="w")
            self.entries[field] = entry

        for col, (label, field, width) in enumerate(fields_group2):
            tk.Label(entry_frame, text=label+":").grid(row=1, column=col*2, padx=5, sticky="e")
            entry = tk.Entry(entry_frame, width=width)
            entry.grid(row=1, column=col*2+1, padx=5, sticky="w")
            self.entries[field] = entry

        for col, (label, field, width) in enumerate(fields_group3):
            tk.Label(entry_frame, text=label+":").grid(row=2, column=col*2, padx=5, sticky="e")
            entry = tk.Entry(entry_frame, width=width)
            entry.grid(row=2, column=col*2+1, padx=5, sticky="w")
            self.entries[field] = entry

        btn_frame = tk.Frame(entry_frame)
        btn_frame.grid(row=3, column=4, columnspan=2, padx=10, sticky="e")
        
        tk.Button(btn_frame, text="清空表单", command=self.clear_entries, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="添加图书", command=self.single_book_entry, width=10).pack(side="left", padx=5)
        tk.Button(entry_frame, text="批量入库", command=self.batch_book_from_path, width=10).grid(row=3, column=6, padx=10)

        tk.Button(main_frame, text="返回主菜单", command=self.show_main_menu, width=15).grid(row=3, column=3, pady=20, sticky="e")

        main_frame.grid_columnconfigure(3, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        self.refresh_book_list()

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def refresh_book_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT BookNo, BookName, BookType, Author, Publisher, Year, Price, Storage FROM Books")
                for row in cursor.fetchall():
                    self.tree.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("错误", f"加载数据失败: {str(e)}")
            finally:
                conn.close()

    def single_book_entry(self):
        required_fields = {
            "book_no": "书号",
            "book_name": "书名",
            "category": "类别",
            "author": "作者",
            "publisher": "出版社",
            "year": "出版年份",
            "price": "价格",
            "quantity": "入库数量"
        }
        
        data = {}
        errors = []

        for field, label in required_fields.items():
            value = self.entries[field].get().strip()
            if not value:
                errors.append(f"{label}不能为空")
            data[field] = value

        if errors:
            messagebox.showwarning("输入错误", "\n".join(errors))
            return

        try:
            data["year"] = int(data["year"])
            data["price"] = float(data["price"])
            data["quantity"] = int(data["quantity"])
            
            if data["year"] < 1800 or data["year"] > 2025:
                raise ValueError("年份必须在1800到2025之间")
            if data["price"] <= 0:
                raise ValueError("价格必须大于0")
            if data["quantity"] <= 0:
                raise ValueError("入库数量必须大于0")
                
        except ValueError as e:
            messagebox.showerror("格式错误", str(e))
            return


        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT BookName FROM Books WHERE BookNo = %s", (data["book_no"],))
            existing_book_by_no = cursor.fetchone()
            
            cursor.execute("SELECT BookNo FROM Books WHERE BookName = %s", (data["book_name"],))
            existing_book_by_name = cursor.fetchone()


            if existing_book_by_no:
                if existing_book_by_no[0] != data["book_name"]:
                    messagebox.showerror("错误", "书号与书名应一一对应")
                    return
            elif existing_book_by_name:
                if existing_book_by_name[0] != data["book_no"]:
                    messagebox.showerror("错误", "书号与书名应一一对应")
                    return

            if existing_book_by_no:
                cursor.execute("""
                    UPDATE Books 
                    SET Storage = Storage + %s 
                    WHERE BookNo = %s
                """, (data["quantity"], data["book_no"]))
            else:
                cursor.execute("""
                    INSERT INTO Books 
                    (BookNo, BookName, BookType, Author, Publisher, Year, Price, Storage)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data["book_no"], data["book_name"], data["category"],
                    data["author"], data["publisher"], data["year"],
                    data["price"], data["quantity"]
                ))

            conn.commit()
            messagebox.showinfo("成功", "操作已完成")
            self.refresh_book_list()
            self.clear_entries()

        except mysql.connector.Error as err:
            if "Duplicate entry" in str(err):
                if "BookNo" in str(err):
                    messagebox.showerror("错误", "书号与书名应一一对应")
                elif "BookName" in str(err):
                    messagebox.showerror("错误", "书号与书名应一一对应")
                else:
                    messagebox.showerror("错误", "书号与书名应一一对应")
            else:
                messagebox.showerror("数据库错误", f"操作失败: {err}")

        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()

    def batch_book_from_path(self):
        
        path = filedialog.askopenfilename(
            filetypes=[("txt文件", "*.txt")],
            title="选择批量入库文件"
        )
        if path:
            self.handle_txt(path)
            # messagebox.showinfo("提示", f"已选择文件：{path}\n")
            self.refresh_book_list()

    def handle_txt(self, path):
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            success_count = 0
            total_count = 0

            with open(path, "r", encoding="utf-8") as file:
                for line_num, line in enumerate(file, 1):
                    total_count += 1
                    line = line.strip()
                    if not line:
                        continue 

                    arr = [field.strip() for field in line.split(",")]
                    if len(arr) != 8:
                        messagebox.showerror(
                            "格式错误",
                            f"第{line_num}行字段数量不正确\n"
                            f"应为8个字段，实际得到{len(arr)}个\n"
                            f"行内容：{line}"
                        )
                        conn.rollback()
                        return

                    data = {}
                    try:
                        data["book_no"] = arr[0]
                        data["book_name"] = arr[1]
                        data["category"] = arr[2]
                        data["author"] = arr[3]
                        data["publisher"] = arr[4]
                        data["year"] = int(arr[5])
                        data["price"] = float(arr[6])
                        data["quantity"] = int(arr[7])
                    except ValueError as e:
                        messagebox.showerror(
                            "数据错误",
                            f"第{line_num}行数据格式错误：\n"
                            f"行内容：{line}\n"
                            f"详细错误：{str(e)}"
                        )
                        conn.rollback()
                        return

                    required_fields = {
                        "book_no": "书号",
                        "book_name": "书名",
                        "category": "类别",
                        "author": "作者",
                        "publisher": "出版社"
                    }
                    missing = [v for k, v in required_fields.items() if not data[k]]
                    if missing:
                        messagebox.showerror(
                            "数据错误",
                            f"第{line_num}行缺少必填字段：\n"
                            f"缺失字段：{', '.join(missing)}\n"
                            f"行内容：{line}"
                        )
                        conn.rollback()
                        return

                    if data["year"] < 1800 or data["year"] > 2025:
                        messagebox.showerror("年份错误", f"第{line_num}行的年份必须在1800到2025之间")
                        conn.rollback()
                        return
                    elif data["price"] <= 0:
                        messagebox.showerror("价格错误", f"第{line_num}行的价格不得低于或等于0")
                        conn.rollback()
                        return
                    elif data["quantity"] <= 0:
                        messagebox.showerror("数量错误", f"第{line_num}行的数量不得低于或等于0")
                        conn.rollback()
                        return

                    try:
                        cursor.execute("SELECT BookName FROM Books WHERE BookNo = %s", (data["book_no"],))
                        existing_book_by_no = cursor.fetchone()
                        
                        cursor.execute("SELECT BookNo FROM Books WHERE BookName = %s", (data["book_name"],))
                        existing_book_by_name = cursor.fetchone()


                        if existing_book_by_no:
                            if existing_book_by_no[0] != data["book_name"]:
                                messagebox.showerror("错误", "书号与书名应一一对应")
                                success_count-=1
                                return 
                        elif existing_book_by_name:
                            if existing_book_by_name[0] != data["book_no"]:
                                messagebox.showerror("错误", "书号与书名应一一对应")
                                success_count-=1
                                return 

                        if existing_book_by_no:
                            cursor.execute("""
                                UPDATE Books 
                                SET Storage = Storage + %s 
                                WHERE BookNo = %s
                            """, (data["quantity"], data["book_no"]))
                        else:
                            cursor.execute("""
                                INSERT INTO Books 
                                (BookNo, BookName, BookType, Author, Publisher, Year, Price, Storage)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                data["book_no"], data["book_name"], data["category"],
                                data["author"], data["publisher"], data["year"],
                                data["price"], data["quantity"]
                            ))
                        conn.commit()
                        success_count += 1

                    except mysql.connector.Error as err:
                        conn.rollback()
                        if "Duplicate entry" in str(err):
                            messagebox.showerror(
                                "错误",
                                f"第{line_num}行：书号或书名已存在且不匹配\n错误详情：{err}"
                            )
                        else:
                            messagebox.showerror(
                                "数据库错误",
                                f"第{line_num}行操作失败: {err}"
                            )
                        return
                    except Exception as e:
                        conn.rollback()
                        messagebox.showerror(
                            "意外错误",
                            f"第{line_num}行处理时发生错误: {str(e)}"
                        )
                        return

            messagebox.showinfo(
                "完成",
                f"批量导入完成！成功处理{success_count}/{total_count}条记录。"
            )

        except FileNotFoundError:
            messagebox.showerror("文件错误", "指定的文件不存在")
        except PermissionError:
            messagebox.showerror("权限错误", "没有权限读取文件")
        except UnicodeDecodeError:
            messagebox.showerror("编码错误", "文件编码不正确，请使用UTF-8编码")
        except Exception as e:
            messagebox.showerror("意外错误", f"发生未预期的错误: {str(e)}")
            if conn:
                conn.rollback()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            self.refresh_book_list()
                

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
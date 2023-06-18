import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import KNN
classes = {1 :"building_windows_float_processed",
     2 :"building_windows_non_float_processed",
     3 :"vehicle_windows_float_processed",
     4 :"vehicle_windows_non_float_processed (none in this database)",
     5 :"containers",
     6 :"tableware",
     7 :"headlamps"}
root = tk.Tk()
root.title("KNN - new model")
root.geometry("1200x900")
root.iconbitmap("./Assets/AI.ico")

train_set = (())
test_set= (())
def ask_for_training_set():
    file_path = filedialog.askopenfilename()
    global train_set
    train_set = KNN.load_data(file_path)
    return [train_set[0][i] + [train_set[1][i]] for i in range(len(train_set[0]))]

def ask_for_test_set():
    file_path = filedialog.askopenfilename()
    global test_set
    test_set = KNN.load_data(file_path)
    return [test_set[0][i] + [test_set[1][i]] for i in range(len(test_set[0]))]

def load_bottom_frame(dimensions):
    global entries
    entries = []
    num_columns = 3
    for i in range(1, dimensions+1):
        atr_label = tk.Label(bottom_frame, text=i)
        atr_entry = tk.Entry(bottom_frame)
        atr_label.grid(row=i, column=1, sticky="w")
        atr_entry.grid(row=i, column=2, sticky="we")
        entries.append(atr_entry)
    # Configure the grid to expand properly
    bottom_frame.columnconfigure(0, weight=1)
    bottom_frame.columnconfigure(num_columns, weight=1)
def display_data(data, table):
    table["columns"] = tuple(range(len(data[0])))
    table.column("#0", width=0, stretch=tk.NO)

    for i in range(len(data[0])):
        table.column(i, width=70, anchor="center", stretch=tk.NO)
        table.heading(i, text=f"Attribute {i+1}")

    for row in data:
        table.insert("", "end", values=tuple(row))

def show_testing_tools(show = True):
    if show:
        right_frame.pack(side="right", padx=10, pady=10)
        right_frame.pack_propagate(False)
        right_frame.configure(width=600, height=450)
        bottom_frame.pack(side="bottom")
        load_bottom_frame(KNN_model.model.n_features_in_)
    else:
        right_frame.pack_forget()
        bottom_frame.pack_forget()
def handle_train_button_click():
    KNN_model.train(train_set)
    show_testing_tools()
def handle_test_button_click():
    accuracy, precision, recall, f1 = KNN_model.test(test_set)
    scores_label.config(text=f"Accuracy: {accuracy}\n"
                             f"Precision {precision}\n"
                             f"Recall: {recall}\n"
                             f"F-score:{f1}\n")
def handle_save_button_click():
    filename = filedialog.asksaveasfilename(defaultextension= ".pkl", filetypes = (("Model files", "*.pkl"), ("All files", "*.*")))
    root.title(f"KNN - {filename}")
    KNN_model.save_model(filename)
def handle_load_button_click():
    file_path = filedialog.askopenfilename(defaultextension=".pkl")
    if file_path:
        global KNN_model
        KNN_model = KNN.load_model(file_path)
        root.title(f"KNN - {file_path}")
        show_testing_tools()
def handle_new_button_click():
    for col in table_tr["columns"]:
        table_tr.heading(col, text="")
        table_tr.column(col, width=0)
    for col in table_te["columns"]:
        table_te.heading(col, text="")
        table_te.column(col, width=0)
    show_testing_tools(False)
    global KNN_model
    KNN_model = KNN.KNNClassifier()
def handle_classify_button_click():
    global entries
    result_num = KNN_model.classify([float(entry.get()) for entry in entries])
    result_label.config(text=f"Type = {classes[result_num]}")
def on_entry_change(*args):
    global KNN_model
    try:
        KNN_model.model.n_neighbors=int(K_entry.get())
    except ValueError:
        pass

top_frame = tk.Frame(root, bg="#c4c4c4")
top_frame.pack(side=tk.TOP, fill=tk.X)

bottom_frame = tk.Frame(root, bg="#c4c4c4")
bottom_frame.pack(side=tk.BOTTOM)

K_label = tk.Label(root, text="K value:")
K_label.pack()

k_var = tk.IntVar(value=5)
k_var.trace("w", on_entry_change)
K_entry = tk.Entry(root, textvariable=k_var)
K_entry.pack()
KNN_model = KNN.KNNClassifier(5)

left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=10, pady=10)
left_frame.pack_propagate(False)
left_frame.configure(width=600, height=450)

# Training Set Selection Button
table_tr = ttk.Treeview(left_frame)
train_button = tk.Button(left_frame, text="Select Training Set", command=lambda: display_data(ask_for_training_set(),table_tr))
train_button.pack(pady=5, padx=10)
scrollbar_v = tk.Scrollbar(left_frame, orient="vertical", command=table_tr.yview)
scrollbar_v.pack(side="right", fill="y")
scrollbar_h = tk.Scrollbar(left_frame, orient="horizontal", command=table_tr.xview)
scrollbar_h.pack(side="bottom", fill="x")
table_tr.pack(fill="y")
table_tr.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

# Training Button
train_btn = tk.Button(left_frame, text="Train", command=handle_train_button_click)
train_btn.pack()

# Right Frame for Testing Set
right_frame = tk.Frame(root)

# Testing Set Selection Button
table_te = ttk.Treeview(right_frame)
test_button = tk.Button(right_frame, text="Select Testing Set", command=lambda: display_data(ask_for_test_set(),table_te))
test_button.pack(pady=5, padx=10)
scrollbar_v1 = tk.Scrollbar(right_frame, orient="vertical", command=table_te.yview)
scrollbar_v1.pack(side="right", fill="y")
scrollbar_h1 = tk.Scrollbar(right_frame, orient="horizontal", command=table_te.xview)
scrollbar_h1.pack(side="bottom", fill="x")
table_te.pack(fill="y")
table_tr.configure(yscrollcommand=scrollbar_v1.set, xscrollcommand=scrollbar_h1.set)

# Testing Button
test_btn = tk.Button(right_frame, text="Test", command=handle_test_button_click)
test_btn.pack()

scores_label = tk.Label(right_frame, text="")
scores_label.pack()


save_btn = tk.Button(top_frame, text="Save model", command=handle_save_button_click, )
save_btn.pack(side=tk.LEFT)
save_btn = tk.Button(top_frame, text="Load model", command=handle_load_button_click)
save_btn.pack(side=tk.LEFT)
save_btn = tk.Button(top_frame, text="New model", command=handle_new_button_click)
save_btn.pack(side=tk.LEFT)



info_label = tk.Label(bottom_frame, text='''1. RI: refractive index
2. Na: Sodium (4-10)
3. Mg: Magnesium
4. Al: Aluminum
5. Si: Silicon
6. K: Potassium
7. Ca: Calcium
8. Ba: Barium
9. Fe: Iron''',anchor="e", justify=tk.LEFT, background="#c4c4c4")
info_label.grid(rowspan=9,column=0)
entries = []


classify_btn = tk.Button(bottom_frame, text="Classify", command=handle_classify_button_click)
classify_btn.grid(row=4, column=3)

result_label = tk.Label(bottom_frame, text="")
result_label.grid(row=4, column=5)

root.mainloop()
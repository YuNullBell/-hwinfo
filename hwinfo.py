import tkinter as tk
from tkinter import ttk
import wmi


def get_hw_info():
    c = wmi.WMI()
    info = []

    # CPU
    for cpu in c.Win32_Processor():
        info.append(("CPU", cpu.Name.strip(), cpu.Manufacturer.strip()))

    # 主板
    for mb in c.Win32_BaseBoard():
        mfr = mb.Manufacturer.strip() if mb.Manufacturer else "N/A"
        model = mb.Product.strip() if mb.Product else "N/A"
        info.append(("主板", model, mfr))

    # RAM
    for ram in c.Win32_PhysicalMemory():
        capacity_gb = int(int(ram.Capacity) / (1024 ** 3))
        speed = ram.Speed if ram.Speed else "N/A"
        mfr = ram.Manufacturer.strip() if ram.Manufacturer else "N/A"
        label = f"{capacity_gb}GB {speed}MHz"
        info.append(("RAM", label, mfr))

    # GPU
    for gpu in c.Win32_VideoController():
        name = gpu.Name.strip() if gpu.Name else "N/A"
        mfr = gpu.AdapterCompatibility.strip() if gpu.AdapterCompatibility else "N/A"
        info.append(("GPU", name, mfr))

    # DISK
    for disk in c.Win32_DiskDrive():
        model = disk.Model.strip() if disk.Model else "N/A"
        size_gb = int(int(disk.Size) / (1024 ** 3)) if disk.Size else 0
        mfr = disk.Manufacturer.strip() if disk.Manufacturer else "N/A"
        label = f"{model} ({size_gb}GB)"
        info.append(("DISK", label, mfr))

    return info


def main():
    root = tk.Tk()
    root.title("硬件信息")
    root.geometry("700x450")
    root.configure(bg="#1a1a1a")
    root.resizable(False, False)

    # TITLE
    title = tk.Label(
        root, text="💻 PC硬件信息", font=("Microsoft YaHei UI", 20),
        fg="white", bg="#1a1a1a"
    )
    title.pack(pady=(25, 20))

    # 表格容器
    frame = tk.Frame(root, bg="#1a1a1a")
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

    tree = ttk.Treeview(
        frame, columns=("item", "value"), show="headings",
        selectmode="none"
    )
    tree.heading("item", text="硬件", anchor="center")
    tree.heading("value", text="SPEC", anchor="w")

    # SIZE
    tree.column("item", width=120, anchor="center")
    tree.column("value", width=450)

    # SCROLLBAR
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # STYLE
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#2d2d2d",
        foreground="white",
        fieldbackground="#2d2d2d",
        borderwidth=0,
        font=("Microsoft YaHei UI", 11),
    )
    style.configure(
        "Treeview.Heading",
        background="#404040",
        foreground="white",
        font=("Microsoft YaHei UI", 12, "bold"),
        borderwidth=0,
    )

    data = get_hw_info()
    for item_name, value, mfr in data:
        tree.insert("", tk.END, values=(item_name, f"{value}  |  制造商: {mfr}"))

    root.mainloop()


if __name__ == "__main__":
    main()

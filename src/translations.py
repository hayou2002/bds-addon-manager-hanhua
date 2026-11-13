# English -> Simplified Chinese for user-facing strings.
# Applied to GDScript string constants and to scene VARIANT_STRING values.

TRANS = {
    # --- dialogs / buttons ---
    "Accept": "接受",
    "Cancel": "取消",
    "OK": "确定",
    "Save": "保存",
    "Delete": "删除",
    "Don't Save": "不保存",
    "Delete pack?": "删除附加包？",
    "Delete failed": "删除失败",
    "Could not delete folder:\n%s": "无法删除文件夹：\n%s",
    "Save changes?": "保存更改？",
    "Unload world?": "卸载世界？",
    "Do you want to unload world: ": "确定要卸载世界：",
    "?\nAny unsaved changes will be lost!": "？\n所有未保存的更改都将丢失！",
    "Close without saving?": "不保存就关闭？",
    "World '": "世界“",
    "' has unsaved changes! Are you sure you want to exit?": "”有未保存的更改！确定要退出吗？",
    "Apply active packs to this world?\nThis will overwrite the currently active packs.":
        "将已启用的附加包应用到该世界？\n这会覆盖当前已启用的附加包。",
    "Apply active packs to this world?\nThis will overwrite the currently active packs.\nWarning: Server is online! Here be dragons!":
        "将已启用的附加包应用到该世界？\n这会覆盖当前已启用的附加包。\n警告：服务器正在运行！风险自负！",

    # --- messages ---
    "No world selected. Choose a world first.": "未选择世界，请先选择一个世界。",
    "Select a world first!": "请先选择一个世界！",
    "No behavior packs detected :(": "未检测到行为包 :(",
    "No resource packs detected :(": "未检测到资源包 :(",
    "Nothing here...yet!": "这里还什么都没有……",
    "Recent worlds list has been disabled": "最近世界列表已禁用",
    "Duplicate pack(s) detected. Skipping.": "检测到重复的附加包，已跳过。",
    "Successfully unloaded world.": "已成功卸载世界。",
    "An unexpected error has occured.": "发生了意外错误。",
    "Successfully loaded world: ": "已成功加载世界：",
    "Saved world: ": "已保存世界：",
    "Failed to save packs for: ": "保存附加包失败：",
    "Warning: empty paths detected!": "警告：检测到空路径！",
    "Error: Invalid resource_packs directory!": "错误：resource_packs 目录无效！",
    "Error: Invalid behavior_packs directory!": "错误：behavior_packs 目录无效！",
    "Error: level.dat not found!": "错误：未找到 level.dat！",
    "Error: Unable to create world pack json file(s)": "错误：无法创建世界附加包的 JSON 文件",
    "Invalid JSON in: ": "JSON 无效：",
    "Invalid Port: Must contain only numbers!": "端口无效：只能包含数字！",
    "Invalid Port: Must be between 1 and 65535!": "端口无效：必须在 1 到 65535 之间！",
    "Invalid format! Enter a valid IP (e.g. 127.0.0.1).": "格式无效！请输入有效的 IP（例如 127.0.0.1）。",
    "Unhide this pack": "取消隐藏此附加包",
    "Hide this pack": "隐藏此附加包",

    # --- world info fragments ---
    " Name: ": " 名称：",
    " - Online": " - 在线",
    " - Offline": " - 离线",
    " Address: ": " 地址：",
    "Unknown": "未知",
    " Gamemode: ": " 游戏模式：",
    " Game version: ": " 游戏版本：",
    "Survival": "生存",
    "Creative": "创造",
    "Adventure": "冒险",
    "Default": "默认",
    " Classic": " 经典",
    " Dark": " 深色",
    " Light": " 浅色",

    # --- file dialog filters ---
    "*.mcpack ; MCPack files": "*.mcpack ; MCPack 文件",
    "*.mcaddon ; MCAddon files": "*.mcaddon ; MCAddon 文件",
    "*.zip ; Zip archives": "*.zip ; Zip 压缩包",

    # --- scene / nav / pages ---
    "World Files": "世界文件",
    "Resource Packs": "资源包",
    "Behavior Packs": "行为包",
    "Import Packs": "导入附加包",
    "Open File(s)": "打开文件",
    "Settings": "设置",
    "Help": "帮助",
    "Placeholder": "占位",
    "Advanced": "高级",
    "Load world": "加载世界",
    "Open file picker": "打开文件选择器",
    " Select world folder...": " 选择世界文件夹…",
    " Select resource pack folder...": " 选择资源包文件夹…",
    " Select behavior pack folder...": " 选择行为包文件夹…",
    " (Optional) Local server IP": "（可选）本地服务器 IP",
    " Port": " 端口",
    "Recently Opened Worlds": "最近打开的世界",
    "Open a Directory": "打开文件夹",
    "Project Site 🡥": "项目主页 🡥",
    "Server Download 🡥": "服务端下载 🡥",
    "Documentation 🡥": "文档 🡥",
    "Program Settings": "程序设置",
    " Hide filtered packs": " 隐藏已过滤的附加包",
    " Hides default server packs and any packs you've chosen to hide":
        " 隐藏默认服务端附加包，以及你选择隐藏的附加包",
    " Hide color formatting": " 隐藏颜色格式代码",
    " Hide '§' text modifiers from pack names": " 从附加包名称中隐藏 '§' 文本修饰符",
    " Recent worlds": " 最近世界",
    " How many saves show up on world selection screen. Set to 0 to disable. \n (Takes effect on restart)":
        " 世界选择界面显示的存档数量。设为 0 可禁用。 \n （重启后生效）",
    "File Management": "文件管理",
    " Avoid pack import conflicts": " 避免附加包导入冲突",
    " Adds a timestamp to imported folder name": " 为导入的文件夹名添加时间戳",
    " Prefer system trash on delete": " 删除时优先使用系统回收站",
    " Try to use the local system trash instead of deleting files immediately ":
        " 尽量使用系统回收站，而不是立即删除文件 ",
    "2024-present by contributors": "2024 至今，由贡献者维护",
    "Do not run this program while server is running!": "请勿在服务器运行时使用本程序！",
    "Quick Actions": "快捷操作",
    "Switch world": "切换世界",
    "Open world folder": "打开世界文件夹",
    "Open config folder": "打开配置文件夹",
    "How to use": "使用说明",
    " Theme": " 主题",
    " Switch the interface color palette": " 切换界面配色方案",
    "No world loaded!": "未加载世界！",
    "Server Information": "服务器信息",
    " Name: World Name - Status": " 名称：世界名称 - 状态",
    " IP address: 127.0.0.1": " IP 地址：127.0.0.1",
    " Gamemode: Survival": " 游戏模式：生存",
    " Game Version: 0.00.000": " 游戏版本：0.00.000",
    "Warning: Do not use this tool while server is running! ":
        "警告：请勿在服务器运行时使用本工具！",
    "Modifying an existing world may result in unexpected behavior. Always make a backup before editing world files!":
        "修改现有世界可能导致意外行为。编辑世界文件前请务必备份！",
    "Selecting a world:": "选择世界：",
    "1. Select the world folder (the one containing the 'level.dat' file).":
        "1. 选择世界文件夹（包含 'level.dat' 文件的那个）。",
    "2. Click the load world button.": "2. 点击加载世界按钮。",
    "3. Software will automatically detect file path validity. If an error occurs, please verify the file path(s).":
        "3. 软件会自动检测文件路径是否有效。如果出错，请检查相应的文件路径。",
    "Managing existing packs": "管理已有的附加包",
    "1. Select the applicable tab from the sidebar.": "1. 从侧边栏选择对应的标签页。",
    "2. Use the arrow buttons to change pack priority. Items on top will take presidence over lower packs.":
        "2. 使用箭头按钮调整附加包优先级。上方的附加包优先于下方的附加包。",
    "3. If a pack contains subpacks, use the dropdown menu to select which subpack is applied.":
        "3. 如果附加包包含子包，使用下拉菜单选择要应用哪个子包。",
    "4. Use the checkbox to enable/disable active packs.": "4. 使用复选框启用/禁用附加包。",
    "5. Right click to hide packs. Toggle hidden packs in settings to view them again. Right click to unhide them.":
        "5. 右键可隐藏附加包。在设置中显示已隐藏的附加包以便再次查看，右键可取消隐藏。",
    "6. Deleting a pack will remove it from your world and disk. This may take some time. Do not close the software while deletion is in progress.":
        "6. 删除附加包会将其从世界和磁盘中移除。这可能需要一些时间，删除过程中请勿关闭软件。",
    "7. Click the save button and confirm to apply changes.": "7. 点击保存按钮并确认以应用更改。",
    "Importing a pack:": "导入附加包：",
    "1. Select the Import Packs button on the sidebar to open the file picker.":
        "1. 点击侧边栏的“导入附加包”按钮以打开文件选择器。",
    "2. Valid pack formats include: .mcpack, .mcaddon, and .zip archives.":
        "2. 有效的附加包格式包括：.mcpack、.mcaddon 和 .zip 压缩包。",
    "3. Depending on pack size, this may take some time. Do not close the software while pack import is in progress.":
        "3. 视附加包大小，这可能需要一些时间。导入过程中请勿关闭软件。",
    "This is where an alert message would appear.": "这里是提示信息的显示位置。",
    "BDS ADDON MANAGER": "BDS 附加包管理器",
    "BDS Addon Manager\n©2024-present by contributors\nDo not run this program while server is running!":
        "BDS 附加包管理器\n©2024 至今，由贡献者维护\n请勿在服务器运行时使用本程序！",

    # --- help screen (single big scene string) ---
    "Warning: Do not use this tool while server is running! \nModifying an existing world may result in unexpected behavior. Always make a backup before editing world files!\n\nSelecting a world:\n1. Select the world folder (the one containing the 'level.dat' file).\n2. Click the load world button.\n3. Software will automatically detect file path validity. If an error occurs, please verify the file path(s).\n\nManaging existing packs\n1. Select the applicable tab from the sidebar.\n2. Use the arrow buttons to change pack priority. Items on top will take presidence over lower packs.\n3. If a pack contains subpacks, use the dropdown menu to select which subpack is applied.\n4. Use the checkbox to enable/disable active packs.\n5. Right click to hide packs. Toggle hidden packs in settings to view them again. Right click to unhide them.\n6. Deleting a pack will remove it from your world and disk. This may take some time. Do not close the software while deletion is in progress.\n7. Click the save button and confirm to apply changes.\n\nImporting a pack:\n1. Select the Import Packs button on the sidebar to open the file picker.\n2. Valid pack formats include: .mcpack, .mcaddon, and .zip archives.\n3. Depending on pack size, this may take some time. Do not close the software while pack import is in progress.\n\n\n":
        "警告：请勿在服务器运行时使用本工具！\n修改现有世界可能导致意外行为。编辑世界文件前请务必备份！\n\n选择世界：\n1. 选择世界文件夹（包含 'level.dat' 文件的那个）。\n2. 点击加载世界按钮。\n3. 软件会自动检测文件路径是否有效。如果出错，请检查相应的文件路径。\n\n管理已有的附加包\n1. 从侧边栏选择对应的标签页。\n2. 使用箭头按钮调整附加包优先级。上方的附加包优先于下方的附加包。\n3. 如果附加包包含子包，使用下拉菜单选择要应用哪个子包。\n4. 使用复选框启用/禁用附加包。\n5. 右键可隐藏附加包。在设置中显示已隐藏的附加包以便再次查看，右键可取消隐藏。\n6. 删除附加包会将其从世界和磁盘中移除。这可能需要一些时间，删除过程中请勿关闭软件。\n7. 点击保存按钮并确认以应用更改。\n\n导入附加包：\n1. 点击侧边栏的“导入附加包”按钮以打开文件选择器。\n2. 有效的附加包格式包括：.mcpack、.mcaddon 和 .zip 压缩包。\n3. 视附加包大小，这可能需要一些时间。导入过程中请勿关闭软件。\n\n\n",
}

# Scripts whose string constants must NOT be translated (structural names).
SKIP_SCRIPT_FILES = {"src/autoload/themes.gdc"}

# Strings that must never be translated even if present (logic keys / identifiers).
NEVER = set()

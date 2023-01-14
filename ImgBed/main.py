from QuickStart_Rhy.SystemTools.FileHash import md5
from QuickStart_Rhy.TuiTools.Table import qs_default_table
from QuickProject.Commander import Commander
from . import _ask
from . import *
import os


app = Commander("img-bed", True)
source = config.select("source")
api = (
    requirePackage("QuickStart_Rhy.API.TencentCloud", "TxCOS")()
    if source == "Tencent Cloud"
    else requirePackage("QuickStart_Rhy.API.AliCloud", "AliyunOSS")()
)


def parseMarkdownImages(markdown_file_path: str):
    import re

    with open(markdown_file_path, "r") as f:
        ct = f.read()
    aims = re.findall("!\[.*?]\((.*?)\)", ct, re.M) + re.findall(
        '<img.*?src="(.*?)".*?>', ct, re.M
    )
    return ct, aims


def apiUploadOneImage(imgPath: str):
    cosName = md5(imgPath)
    _lt = os.path.basename(imgPath)
    _lt = "." + _lt.lower().split(".")[-1] if "." in _lt else ""

    start_url = config.select("url").rstrip("/")
    start_path = "/".join(start_url.split("://")[1].split("/")[1:]) + "/"

    api.upload(imgPath, key=start_path + cosName + _lt)
    return start_url + "/" + cosName + _lt


def formatAbsPath(img, rt_path, user_root):
    """
    计算图片的绝对路径 (Mac、Windows、Linux通用)

    :param img: 图片路径
    :param rt_path: Markdown文件所在目录
    :param user_root: 用户根目录
    """
    if img[0] == "~":
        return os.path.join(user_root, img.lstrip("~"))
    return img if os.path.abspath(img) == img else os.path.abspath(rt_path + img)


@app.command()
def markdown(filepath: str):
    """
    解析Markdown文件中的图片链接上传至图床并替换路径为链接

    :param filepath: Markdown文件路径
    """
    from QuickStart_Rhy.TuiTools.Bar import NormalProgressBar
    from QuickProject import QproWarnString
    from QuickStart_Rhy import user_root

    rt_path = os.path.dirname(os.path.abspath(filepath))
    uploaded = {}
    ct, imgs = parseMarkdownImages(filepath)
    table = qs_default_table(["本地文件", "链接"], title="映射表\n")
    progress, task_id = NormalProgressBar("上传并替换图片", len(imgs))
    progress.start()
    progress.start_task(task_id)
    for img in imgs:
        if img.startswith("http://") or img.startswith("https://"):
            progress.advance(task_id, 1)
            QproDefaultConsole.print(QproWarnString, img, "不是本地文件")
            continue
        _raw = img
        img = formatAbsPath(img, rt_path, user_root)
        if img not in uploaded:
            url = apiUploadOneImage(img)
            table.add_row(f"[bold magenta]{img}[/]", f"[bold cyan]{url}[/]")
            uploaded[img] = url

        ct = ct.replace(_raw, uploaded[img])
        progress.advance(task_id, 1)
    progress.stop()
    with open(filepath, "w") as f:
        f.write(ct)
    QproDefaultConsole.print(table, justify="center")


@app.command()
def add(files: list):
    """
    上传多个图片至腾讯云存储图床

    :param files: 图片文件路径列表
    """
    table = qs_default_table(["本地文件", "链接"], title="映射表")
    for file in files:
        if not os.path.isfile(file):
            continue
        url = apiUploadOneImage(file)
        table.add_row(f"[bold magenta]{file}[/]", f"[bold cyan]{url}[/]")
    if len(files) == 1:
        requirePackage("pyperclip", "copy")(url)
        QproDefaultConsole.print(QproInfoString, "已复制链接到剪贴板")
    QproDefaultConsole.print(table, justify="center")
    if len(files) == 1 and _ask(
        {"type": "confirm", "message": "是否删除本地文件?", "name": "rm", "default": True}
    ):
        requirePackage("QuickStart_Rhy", "remove")(files[0])


def main():
    app()


if __name__ == "__main__":
    main()

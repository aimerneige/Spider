# WallpaperCave

最后测试时间：2020年4月3日

---

需要安装的第三方库

- requests

---

只提供了接口，不能直接使用

某接口使用示例

```python
search_result = search("ddlc")
for sr in search_result:
    wall_link_parse_result = wallpaper_link_parse(sr['url'])
    print(wall_link_parse_result)
    exit()
    all_download_link = get_download_link(wall_link_parse_result)
    with open("link.txt", 'a') as f:
        f.write(all_download_link)
```

结果：

获得下载链接组成的txt文件，然后可以使用多线程下载工具（如uget）进行下载。

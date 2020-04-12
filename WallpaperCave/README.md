# WallpaperCave

最后测试时间：2020年4月3日

---

需要安装的第三方库

- requests

---

某使用示例

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

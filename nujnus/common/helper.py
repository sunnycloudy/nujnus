def helper(desc, demo):
    return "{}:{}".format(
        custom_ljust(shorten_string(desc, 20), 20, "."), shorten_string(demo, 100)
    )


def command_desc(commandname, desc, sp="|"):
    return "{}{}{}".format(
        custom_rjust(shorten_string(commandname, 20), 20, " "),
        sp,
        shorten_string(desc, 100),
    )


# 纯英文的情况:
# def shorten_string(s, limit):
#    """如果字符串长度超过30个字符，缩短到30个字符并在末尾添加三个点"""
#    if len(s) > limit:
#        return s[: limit - 3] + "..."
#    else:
#        return s


# 中英文混合的情况:
def shorten_string(s, limit):
    """
    如果字符串的显示长度超过限制，则缩短它，并在末尾添加三个点。
    参数s是要处理的字符串，limit是显示长度的限制。
    """

    actual_width = unicode_width(s)
    # 计算字符串s的显示宽度。这里假设中文字符宽度为2，英文字符宽度为1。

    if actual_width > limit:
        # 如果字符串的显示宽度超过了限制，
        # 则开始找到合适的位置进行截断，以保持总宽度不超过限制。

        current_width = 0
        # 初始化当前累计宽度为0。

        for i, char in enumerate(s):
            # 遍历字符串s中的每个字符及其索引。

            char_width = 2 if "\u4e00" <= char <= "\u9fff" else 1
            # 如果字符是中文（根据Unicode码点判断），则其宽度计为2；否则，计为1。

            if current_width + char_width > limit - 3:
                # 如果当前累计宽度加上当前字符的宽度超过了限制宽度减去3
                # （这里减去3是为了留出空间给"..."），
                # 则在当前位置截断字符串，并在末尾添加"..."。

                return s[:i] + "..."
                # 返回截断后的字符串加上"..."。

            current_width += char_width
            # 更新当前累计宽度。

    else:
        # 如果字符串的显示宽度未超过限制，则直接返回原字符串。
        return s


def unicode_width(s):
    """计算字符串的显示宽度，假设中文字符宽度为2，英文字符宽度为1"""
    return sum(2 if "\u4e00" <= c <= "\u9fff" else 1 for c in s)


def custom_ljust(s, width, fillchar=" "):
    """左对齐字符串，使中英文字符等宽处理"""
    actual_width = unicode_width(s)
    fill_width = max(0, width - actual_width)
    return s + fillchar * fill_width

def custom_rjust(s, width, fillchar=" "):
    """左对齐字符串，使中英文字符等宽处理"""
    actual_width = unicode_width(s)
    fill_width = max(0, width - actual_width)
    return fillchar * fill_width + s


def title(name):
    width = 32 + unicode_width(name)
    print("#" * width)
    print("#" + " " * (width - 2) + "#")
    print("#" + " " * 15 + name + " " * 15 + "#")
    print("#" + " " * (width - 2) + "#")
    print("#" * width)

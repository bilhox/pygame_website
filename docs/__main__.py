import xml.etree.ElementTree as ET

PYGAME_CE_START_VERSION = 0b000000100000000100000011

def pygame_name(version : str) -> bool:
    n_version = [int(n) for n in version.split(".")]
    byte_version = 0
    for n in n_version:
        byte_version = (byte_version << 8) + n
    
    return "pygame" if byte_version < PYGAME_CE_START_VERSION else "pygame-ce"

def parse_description(raw_content : str) -> str:
    index = raw_content.find("```")
    tag_end = False
    while index != -1:
        if not tag_end:
            raw_content = raw_content.replace("```", "<pre class=\"language-python\"><code class=\"code-sample\">", 1)
        else:
            raw_content = raw_content.replace("```", "</code></pre>", 1)
        tag_end = not tag_end
        index = raw_content.find("```")

    index = raw_content.find("``")
    tag_end = False
    while index != -1:
        if not tag_end:
            raw_content = raw_content.replace("``", "<code>", 1)
        else:
            raw_content = raw_content.replace("``", "</code>", 1)
        tag_end = not tag_end
        index = raw_content.find("``")

    raw_content = raw_content.split("\n")
    lines = []
    to_be_stripped = True
    for line in raw_content:
        if to_be_stripped:
            line = line.strip()
            lines.append(line)
            if "<pre class=\"language-python\">" in line:
                to_be_stripped = False
        else:
            if line.strip() == "</code></pre>":
                to_be_stripped = True
                lines.append(line.strip())
                continue
            lines.append(line)

    lines.append("")
    new_doc = "<div>"
    p_tag_closed = True
    doc_type = "text"
    for n , line in enumerate(lines):
        if line == '':
            p_tag_closed = True
            if doc_type == "text":
                new_doc += "</p>"
            elif doc_type != "code-sample":
                new_doc += "</p></div>"
            new_doc += "\n"
        else:
            white_space = True
            if(p_tag_closed):
                if(".. versionadded:: " in line):
                    doc_type = "new"
                    new_doc += "<div class=\"new-feature\"><p>"
                    message_start_index = line.find(" ",len(".. versionadded:: "))
                    version = line[len(".. versionadded:: "):message_start_index]
                    line = f"<u>New in {pygame_name(version)} " + version + ":</u>" + line[message_start_index:]
                elif (".. versionchanged:: " in line):
                    doc_type = "updated"
                    new_doc += "<div class=\"updated\"><p>"
                    message_start_index = line.find(" ",len(".. versionchanged:: "))
                    version = line[len(".. versionchanged:: "):message_start_index]
                    line = f"<u>Changed in {pygame_name(version)} " + version + ":</u>" + line[message_start_index:]
                elif ("<pre class=\"language-python\">" in line):
                    doc_type = "code-sample"
                else:
                    doc_type = "text"
                    new_doc += "<p>"

                white_space = False
                p_tag_closed = False
            
            if doc_type == "code-sample":
                new_doc += "\n"+line
                continue

            new_doc += " "*white_space + line
    
    return new_doc+"</div>"

def find_with_tag_and_class(node : ET.Element, tag : str, classname : str) -> ET.Element:

    for nod in node.findall(tag):
        if nod.attrib["class"] == classname:
            return nod

def load_node(node : ET.Element, doc_node : ET.Element, parent : ET.Element, doc_parent : ET.Element) -> None:

    if not doc_parent:
        node.tag = "div"
        node.attrib["id"] = "doc-content"
        return

    if(doc_node.tag == "section" and doc_node.attrib["type"] == "module"):
        node.tag = "div"
        node.attrib["class"] = "module-display"
        
        header = ET.Element("div")
        header.attrib["class"] = "module-header"

        module_members = ET.Element("div")
        module_members.attrib["class"] = "module-members"

        module_members_title = ET.Element("h3")
        module_members_title.attrib["class"] = "module-members-title"
        module_members_title.text = "Module members"
        module_members.append(module_members_title)

        member_list = ET.Element("ul")

        for member in doc_node.findall("member"):
            name = member.find("name").text
            name = name[0:len(name)-2] if "()" in name else name
            short_description = member.find("short-description").text

            member_tag = ET.Element("li")
            code_tag = ET.Element("code")
            prototype_link = ET.Element("a", {"href":f"test.html#{name}"})
            prototype_link.text = name
            code_tag.append(prototype_link)
            member_tag.append(code_tag)

            desc_ul = ET.Element("ul")
            desc_li = ET.Element("li")
            desc_li.text = short_description
            desc_ul.append(desc_li)
            member_tag.append(desc_ul)

            member_list.append(member_tag)

        module_members.append(member_list)
        node.append(header)
        node.append(module_members)
        
        parent.append(node)
    
    elif doc_parent.tag == "section":

        if doc_node.tag == "name":

            node.tag = "h1"
            node.attrib["class"] = "module-title"
            node.text = doc_node.text

            header = find_with_tag_and_class(parent, "div", "module-header")
            header.append(node)
        
        elif doc_node.tag == "short-description":

            node.tag = "p"
            node.text = doc_node.text

            header = find_with_tag_and_class(parent, "div", "module-header")
            header.append(node)
        
        elif doc_node.tag == "description":
            node = ET.fromstring(parse_description(doc_node.text.strip()))

            node.attrib["class"] = "module-description"
            
            parent.append(node)
        
        elif doc_node.tag == "member":

            node.tag = "div"
            node.attrib["class"] = "m-documentation"

            m_title_container = ET.Element("div")
            m_title_container.attrib["class"] = "m-title-container"
            node.append(m_title_container)

            m_description = ET.Element("div")
            m_description.attrib["class"] = "m-description"
            node.append(m_description)

            parent.append(node)
    
    elif doc_parent.tag == "member":

        if doc_node.tag == "name":

            node.tag = "code"
            node.attrib["class"] = "m-code"
            node.text = doc_node.text

            m_title_container = find_with_tag_and_class(parent, "div", "m-title-container")
            m_title_container.attrib["id"] = doc_node.text[0:len(doc_node.text)-2] if "()" in doc_node.text else doc_node.text
            m_title_container.append(node)
        
        elif doc_node.tag == "short-description":

            node.tag = "p"
            node.attrib["class"] = "m-short-description"
            node.text = doc_node.text

            m_description = find_with_tag_and_class(parent, "div", "m-description")
            m_description.append(node)
        
        elif doc_node.tag == "prototype":

            pre = ET.Element("pre")
            pre.attrib["class"] = "language-python"

            node.tag = "code"
            node.attrib["class"] = "m-doctype"
            node.text = doc_node.text

            pre.append(node)
            
            m_description = find_with_tag_and_class(parent, "div", "m-description")
            m_description.append(pre)
        
        elif doc_node.tag == "description":

            node = ET.fromstring(parse_description(doc_node.text.strip()))
            node.attrib["class"] = "m-desc"

            m_description = find_with_tag_and_class(parent, "div", "m-description")
            m_description.append(node)


def generate_doc_content(node : ET.Element, doc_parent : ET.Element, parent : ET.Element) -> ET.Element:

    tag_name = ""
    result = ET.Element(tag_name)

    load_node(result, node, parent ,doc_parent)

    for sub_node in node:
        generate_doc_content(sub_node, node, result)

    return result


tree = ET.parse("./ref/display.xml")

docs = tree.getroot()

r = generate_doc_content(docs, None, None)

new_tree = ET.parse("./docs/template.xml")
body = new_tree.getroot().find("body")
body.append(r)
new_tree.write("./generated_pages/test.html", "utf-8")

lines = []
with open("./generated_pages/test.html", "r") as reader:

    rlines = reader.readlines()
    for line in rlines:
        lines.append(line.replace("/>",">"))

with open("./generated_pages/test.html", "w") as writer:
    writer.writelines(lines)
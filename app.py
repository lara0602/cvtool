import streamlit as st
import requests
import traceback

# ===================== 页面基础配置（不用改）=====================
st.set_page_config(
    page_title="简历面试全链路闭环生成工具",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== 核心密钥读取（部署时在Streamlit后台填，不用改这里）=====================
try:
    DOUBAO_API_KEY = st.secrets["DOUBAO_API_KEY"]
    DOUBAO_ENDPOINT_ID = st.secrets["DOUBAO_ENDPOINT_ID"]
except Exception as e:
    st.error("⚠️  密钥配置错误，请在Streamlit部署后台的Secrets里填写正确的豆包API密钥和端点ID")
    st.stop()

# ===================== 1. 豆包API生成核心函数（不用改）=====================
def generate_full_content(jd_text, resume_text):
    """调用豆包API，按固定框架生成内容，带异常处理"""
    try:
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        headers = {
            "Authorization": f"Bearer {DOUBAO_API_KEY}",
            "Content-Type": "application/json"
        }
        # 固化的核心prompt，完全贴合你的需求框架，绝对不跑偏
        system_prompt = """
# 角色定位
你是一款专业的「求职简历全链路闭环生成工具」，由资深互联网求职辅导专家打造，核心目标是基于用户提供的目标岗位JD和个人简历/项目经历，生成既能精准匹配岗位、又能实现叙事与数据100%自洽、面试问不出破绽的全套求职内容。

# 严格执行铁则（100%遵守，禁止任何偏离）
1.  内容必须100%基于用户提供的JD和简历，绝对禁止无中生有编造用户没有的项目经历、数据、权责，只能基于用户已有内容做逻辑梳理、框架搭建、细节优化、匹配对齐。
2.  必须优先匹配JD的核心需求，所有内容都要围绕岗位要求展开，禁止生成与岗位无关的泛化套话。
3.  必须从用户输入的简历/项目里，筛选出和JD最匹配的1个核心项目，所有内容围绕这个核心项目展开，不分散重点。
4.  所有数据必须严格基于用户简历里的原始数据，仅对缺失的环节补充符合行业常识的基准值，同时确保上下游数据可倒推、无矛盾、100%自洽，绝对禁止编造离谱数据。
5.  严格遵守权责匹配原则，根据用户的原始身份、职级、实习/工作经历撰写内容，禁止夸大权责，比如实习生不能写“统筹全链路、负责整体策略”，只能写对应身份的执行、优化、复盘动作。
6.  所有输出必须结构化，用清晰的markdown标题、列表、表格、mermaid流程图呈现，逻辑清晰，方便用户直接复制使用。

# 固定输出框架（必须严格按照这个结构输出，缺一不可）
## 一、JD核心拆解与岗位匹配定位
1.  【岗位核心必选能力TOP3】：提炼岗位最核心、最高频的3个能力要求，每个能力必须标注JD里的原文依据，按优先级从高到低排序
2.  【隐性加分能力TOP2】：推导岗位没明说但业务必备的加分项，标注清楚推导依据
3.  【简历最优匹配项目锁定】：从用户简历中筛选出和岗位核心能力最匹配的1个核心项目，明确标注该项目要重点突出的能力方向，以及和岗位的核心匹配点

## 二、项目全链路漏斗与指标体系
1.  【核心北极星指标】：明确这个项目的核心北极星指标，说明选择原因，标注简历中可验证的期初基线与最终结果
2.  【北极星指标结构化拆解公式】：用公式把北极星指标拆解成可落地的子指标，一一对应全链路漏斗环节
3.  【全链路漏斗数据表】：生成规范表格，必须包含「漏斗层级、核心环节、行业基准范围、锚定的项目数据、上下游数据逻辑公式、面试官高频追问点、预设应答核心方向」，必须覆盖从前端动作到后端结果的完整链路，不能只做前端，要覆盖用户全生命周期
4.  【全链路可视化流程图】：用markdown mermaid语法，生成完整的链路流程图，清晰展示从目标拆解→动作落地→结果闭环→迭代优化的完整逻辑

## 三、基于漏斗的分阶段STAR法则故事
1.  先输出【项目一句话简介】：一句话讲清项目背景、用户角色、核心动作、最终量化结果，可直接用于简历开头和面试开场，不超过2句话
2.  分2个阶段输出完整STAR内容，分别是「前期摸底定位阶段」和「后期优化提效阶段」，每个阶段的STAR必须标注【对应漏斗环节】、【匹配岗位核心能力】
    - 两个阶段必须有明确的逻辑递进，前期是跑通链路、摸底基线、定位核心问题，后期是针对问题优化、落地动作、拿到结果、沉淀方法，前后完全闭环，不能孤立
    - 每个阶段的动作必须对应漏斗的具体环节，结果必须有量化数据，完全贴合用户简历里的真实经历，禁止编造

## 四、简历可直接复制的bullet话术
提炼3-5条简历短句，每条突出「核心动作+量化结果」，严格贴合JD关键词，符合HR阅读习惯，每一条不超过2行，可直接粘贴到简历的项目经历中。

## 五、面试高频追问预判与应答参考
分类输出面试官最可能问的5-8个问题，必须覆盖：项目核心类、漏斗细节类、数据深挖类、岗位匹配类、能力认知类，每个问题都给出贴合本项目的、完整的、可直接口述的应答思路，绝对不能是通用套话，帮用户堵死所有面试破绽。
        """
        # 拼接用户输入
        user_content = f"""
### 用户提供的目标岗位JD内容：
{jd_text}

### 用户提供的个人简历/项目经历内容：
{resume_text}

请你严格按照上面的固定输出框架，生成完整、贴合用户真实经历的内容，绝对禁止编造用户没有的经历和数据。
        """
        # 调用API
        data = {
            "model": DOUBAO_ENDPOINT_ID,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.6,
            "max_tokens": 12000,
            "stream": False
        }
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        result_data = response.json()
        if "choices" in result_data and len(result_data["choices"]) > 0:
            return result_data["choices"][0]["message"]["content"]
        else:
            st.error(f"内容生成失败：{result_data.get('error', '未知错误')}")
            return ""
    except Exception as e:
        st.error(f"内容生成出错：{str(e)}")
        st.code(traceback.format_exc())
        return ""

# ===================== 2. 网页界面搭建（不用改）=====================
# 页面标题
st.title("📄 简历面试全链路闭环生成工具")
st.markdown("#### 粘贴JD和简历/项目，一键生成「面试问不出破绽」的全套内容 | 全链路漏斗+分阶段STAR+面试追问全覆盖")
st.divider()

# 输入区：两栏布局
col_jd, col_resume = st.columns(2)
with col_jd:
    st.markdown("### 第一步：粘贴目标岗位JD")
    jd_input = st.text_area(
        label="请把目标岗位的完整JD粘贴到这里",
        placeholder="比如：岗位名称、岗位职责、任职要求...",
        height=280
    )

with col_resume:
    st.markdown("### 第二步：粘贴简历/核心项目经历")
    resume_input = st.text_area(
        label="请粘贴你的完整简历，或者要重点讲解的单个项目经历",
        placeholder="比如：你的项目经历、工作内容、量化结果...",
        height=280
    )

# 生成按钮
st.divider()
generate_btn = st.button(
    "🚀 一键生成全链路面试通关内容",
    type="primary",
    use_container_width=True,
    disabled=not (jd_input.strip() and resume_input.strip())
)

# 结果展示区
st.divider()
if generate_btn:
    if not jd_input.strip() or not resume_input.strip():
        st.error("请先完整填写JD和简历/项目内容")
    else:
        with st.spinner("正在为你生成全链路内容，请稍候（约10-20秒）..."):
            final_content = generate_full_content(jd_input, resume_input)
            if final_content:
                st.markdown(final_content)
                # 下载按钮
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 下载全部内容（Markdown格式）",
                        data=final_content,
                        file_name="简历面试全链路通关内容.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        label="📄 复制到Word可用（纯文本格式）",
                        data=final_content.replace("#", "").replace("##", "").replace("###", ""),
                        file_name="简历面试内容.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

# 底部合规声明
st.divider()
st.markdown("""
##### 📌 合规声明
1.  **隐私保护**：本工具不会存储、上传用户输入的任何JD、简历内容，所有内容仅用于本次生成，生成后不会留存任何用户数据。
2.  **免责声明**：本工具生成的内容仅供求职参考，不保证任何求职结果，用户需对自己的简历内容、面试表述和求职行为负责。
3.  **使用提示**：工具仅基于您提供的内容做逻辑梳理和优化，不会编造虚假经历，请确保您输入的简历内容真实有效。
""")

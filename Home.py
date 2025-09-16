import streamlit as st

st.set_page_config(
  page_title="  Lumea - Home", 
 layout="wide",
  initial_sidebar_state="collapsed"
)

hide_st_style = """
  <style>
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}
  </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("""
<style>
@keyframes gradient {
  0% {
    background-position: 0% 0%;
  }
  50% {
    background-position: 100% 100%;
  }
  100% {
    background-position: 0% 0%;
  }
}
            
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    height: 100%;
    width: 100%;
    overflow: hidden;
}

body {
  background: transparent;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
            
[data-testid="stApp"] {
    z-index: 1;
    width: auto;
    height: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    align-items: center;
    color: white;
    opacity: 1;
}
[data-testid="stSidebarNavLinkContainer"]{
  backdrop-filter: blur(50px);
  transform: translateY(-20px);             
            
}           
:root {
  --color-bg1: #000042;
  --color-bg2: #262626;
  --color-bg3: #000000;
  --color-bg4: #000068;
  --color1: 0, 0, 252;
  --color2: 74, 92, 255;
  --color3: 0, 157, 255;
  --color4: 0 ,0, 255;
  --color5:  74, 92, 255;
  --color-interactive: 140, 100, 255;
  --circle-size: 80%;
  --blending: hard-light;
}  
             
@keyframes moveInCircle {
  0% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(180deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes moveVertical {
  0% {
    transform: translateY(-50%);
  }
  50% {
    transform: translateY(50%);
  }
  100% {
    transform: translateY(-50%);
  }
}

@keyframes moveHorizontal {
  0% {
    transform: translateX(-50%) translateY(-10%);
  }
  50% {
    transform: translateX(50%) translateY(10%);
  }
  100% {
    transform: translateX(-50%) translateY(-10%);
  }
}
            
.gradient-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    background: linear-gradient(40deg, var(--color-bg1), var(--color-bg2), var(--color-bg3), var(--color-bg4));
    overflow: hidden;
}

svg {
    position: relative;
    top:0;
    left:0;
    width: 0;
    height: 0;
}


.gradients-container {
    filter: url(#goo) blur(40px) ;
    width: 100%;
    height: 100%;
    z-index:1;
  }

.g1 {
    position: absolute;
    background: radial-gradient(circle at center, rgba(var(--color1), 0.8) 0, rgba(var(--color1), 0) 50%) no-repeat;
    mix-blend-mode: var(--blending);

    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2);
    left: calc(50% - var(--circle-size) / 2);

    transform-origin: center center;
    animation: moveVertical 30s ease infinite;

    opacity: 1;
}

.g2 {
    position: absolute;
    background: radial-gradient(circle at center, rgba(var(--color2), 0.8) 0, rgba(var(--color2), 0) 50%) no-repeat;
    mix-blend-mode: var(--blending);

    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2);
    left: calc(50% - var(--circle-size) / 2);

    transform-origin: calc(50% - 400px);
    animation: moveInCircle 20s reverse infinite;

    opacity: 1;
}

.g3 {
    position: absolute;
    background: radial-gradient(circle at center, rgba(var(--color3), 0.8) 0, rgba(var(--color3), 0) 50%) no-repeat;
    mix-blend-mode: var(--blending);

    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2 + 200px);
    left: calc(50% - var(--circle-size) / 2 - 500px);

    transform-origin: calc(50% + 400px);
    animation: moveInCircle 40s linear infinite;

    opacity: 1;
}

.g4 {
    position: absolute;
    background: radial-gradient(circle at center, rgba(var(--color4), 0.8) 0, rgba(var(--color4), 0) 50%) no-repeat;
    mix-blend-mode: var(--blending);

    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2);
    left: calc(50% - var(--circle-size) / 2);

    transform-origin: calc(50% - 200px);
    animation: moveHorizontal 40s ease infinite;

    opacity: 0.7;
}

.g5 {
    position: absolute;
    background: radial-gradient(circle at center, rgba(var(--color5), 0.8) 0, rgba(var(--color5), 0) 50%) no-repeat;
    mix-blend-mode: var(--blending);

    width: calc(var(--circle-size) * 2);
    height: calc(var(--circle-size) * 2);
    top: calc(50% - var(--circle-size));
    left: calc(50% - var(--circle-size));

    transform-origin: calc(50% - 800px) calc(50% + 200px);
    animation: moveInCircle 20s ease infinite;

    opacity: 1;
}
.button-container1 {

    display: flex;
    justify-content: center;
    text-align: center;
    align-items: center;
    gap: 30px; 
    flex-wrap: wrap; 
    padding: 10px 10px 10px 10px;
    margin-top: 50px;
}
.button{
    height: 180px;
    width: 300px;
    color: white !important;
    text-decoration: none !important;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 15px 30px;
    overflow: hidden;
    transition: 0.2s;
}          

.button:hover {
    color: white;
    text-shadow: 0 0 10px #00f0ff;
    box-shadow: 0 0 10px #FF9131, 0 0 40px #6736F3, 0 0 80px #2196f3;
    transform: translateY(-20px);
}

.button *, .button-label1, .button-description1 {
    color: white ;
    text-decoration: none !important; ;
}


.button-label1 {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 10px;
    color: white !important;
}

.button-description1 {
    text-align: center;
    font-size: 18px;
    color: white !important;
}
</style>
<div class="gradient-bg">
  <svg xmlns="http://www.w3.org/2000/svg">
    <defs>
      <filter id="goo">
        <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
        <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8" result="goo" />
        <feBlend in="SourceGraphic" in2="goo" />
      </filter>
    </defs>
  </svg>
  <div class="gradients-container">
    <div class="g1"></div>
    <div class="g2"></div>
    <div class="g3"></div>
    <div class="g4"></div>
    <div class="g5"></div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] > div:first-child {
        
      height:100%;
      width: 100%;
      background-color: #000000; !important;
      backdrop-filter: blur(20px) !important;
       
    </style>
    """,
    unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; font-size: 90px; color: #ffffff; text-shadow: 0 0 20px #00bfff;'> Lumea</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Simplify your hiring process and discover the right talent.</h3>", unsafe_allow_html=True)

st.markdown("""<div style='text-align:center; font-size: 18px; padding-left:15%;padding-right:15%'><b>
            Lumea  is an intelligent resume retrieval system designed to streamline the hiring process by instantly finding the most relevant resumes based
             on a given job description or query. Built using cutting-edge AI technologies, Lumea ensures precision, speed, and efficiency in candidate selection.</b></div>""", unsafe_allow_html=True)
st.markdown("""</br></br>""",unsafe_allow_html=True)
col1,col2,col3=st.columns(3)
with col1:
    st.markdown("""
    <div class="button-container1">
      <div class="button">          
        <a href="/Resume_Finder" >
            <div class="button-label1"> Resume Search</div>
            <div class="button-description1">Find top resumes instantly based on your job description.</div>
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="button-container1">
      <div class="button">
        <a href="/Self_data_recruiter">
         <div class="button-label1">Upload Search</div>
         <div class="button-description1">Upload your own resume files and based on that you can ask questions and <b>Lumea</b> gives the answers</div>
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="button-container1">
      <div class="button">            
        <a href="/AI_enhancer">
            <div class="button-label1">AI Enhencer</div>
            <div class="button-description1">AI gives suggestions to enhance resumes for better impact.</div>
        </a>
      </div>
    </div> 
    """, unsafe_allow_html=True)

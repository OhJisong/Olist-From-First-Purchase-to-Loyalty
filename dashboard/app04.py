import streamlit as st
import pandas as pd
import plotly.express as px

# --- 0. 한글 번역 사전 ---
translation_dict = {
    'health_beauty': '건강/미용', 'computers_accessories': '컴퓨터 액세서리', 'auto': '자동차 용품',
    'bed_bath_table': '침구/욕실', 'furniture_decor': '가구/인테리어', 'sports_leisure': '스포츠/레저',
    'perfumery': '향수', 'housewares': '생활용품', 'telephony': '통신',
    'watches_gifts': '시계/선물', 'food_drink': '식음료', 'baby': '유아용품',
    'stationery': '문구', 'tablets_printing_image': '태블릿/인쇄', 'toys': '장난감',
    'cool_stuff': '쿨스터프', 'garden_tools': '정원도구', 'pet_shop': '펫샵',
    'electronics': '전자기기', 'construction_tools_construction': '건설도구',
    'home_appliances': '가전제품', 'consoles_games': '콘솔/게임', 'computers': '컴퓨터',
    'home_confort': '홈 컴포트', 'fixed_telephony': '유선전화', 'industry_commerce_and_business': '산업/상업',
    'home_appliances_2': '가전제품 2', 'signaling_and_security': '신호/보안', 'musical_instruments': '악기',
    'small_appliances': '소형가전', 'art': '예술', 'fashion_bags_accessories': '패션 잡화',
    'home_construction': '주택 건설', 'costruction_tools_tools': '건설 공구',
    'luggage_accessories': '여행가방/액세서리', 'market_place': '마켓플레이스',
    'construction_tools_lights': '건설 조명', 'office_furniture': '사무용 가구',
    'agro_industry_and_commerce': '농업/산업', 'air_conditioning': '냉난방',
    'books_general_interest': '교양서적', 'kitchen_dining_laundry_garden_furniture': '주방/정원 가구',
    'fashion_shoes': '패션 신발', 'books_technical': '기술서적',
    'construction_tools_safety': '건설 안전', 'food': '식품', 'drinks': '음료',
    'home_comfort_2': '홈 컴포트 2', 'audio': '오디오', 'fashion_male_clothing': '남성 의류',
    'other': '기타', 'dvds_blu_ray': 'DVD/블루레이', 'party_supplies': '파티용품',
    'flowers': '꽃', 'books_imported': '수입서적', 'cine_photo': '영화/사진',
    'fashion_underwear_beach': '속옷/비치웨어', 'music': '음악', 'small_appliances_home_oven_and_coffee': '소형 주방가전',
    'fashion_sport': '스포츠 패션', 'christmas_supplies': '크리스마스 용품', 'fashion_female_clothing': '여성 의류',
    'furniture_bedroom': '침실 가구', 'furniture_living_room': '거실 가구',
    'furniture_mattress_and_upholstery': '매트리스/가구', 'cds_dvds_musicals': 'CD/DVD',
    'costruction_tools_garden': '정원 공구', 'la_cuisine': '라 퀴진', 'diapers_and_hygiene': '기저귀/위생',
    'security_and_services': '보안/서비스', 'pc_gamer': '게이밍 PC', 'insurance_and_services': '보험/서비스',
    'fashion_childrens_clothes': '아동 의류'
}

# --- 1. 데이터 로딩 ---
@st.cache_data
def load_all_data():
    final_kpi_table = pd.read_csv('final_kpi_table.csv')
    final_kpi_table['product_category_name_korean'] = final_kpi_table['product_category_name_english'].map(translation_dict).fillna(final_kpi_table['product_category_name_english'])
    state_kpi_data = pd.read_csv('state_kpi_data.csv')
    cat_state_dist = pd.read_csv('category_state_distribution.csv')
    model_predictions = pd.read_csv('model_predictions_by_state.csv')
    # ★★★ 카테고리별 Before 지도에 사용할 데이터 로딩 ★★★
    category_state_loyal_customers = pd.read_csv('category_state_loyal_customers.csv')
    return final_kpi_table, state_kpi_data, cat_state_dist, model_predictions, category_state_loyal_customers

final_kpi_table, state_kpi_data, cat_state_dist, model_predictions, category_state_loyal_customers = load_all_data()

# --- 2. 시뮬레이션 함수 (Tab 1 용) ---
def marketing_investment_simulator(category_name_english, investment_amount, kpi_df):
    CAC = 30; category_data = kpi_df[kpi_df['product_category_name_english'] == category_name_english].iloc[0]
    result = {"투자 카테고리": category_data['product_category_name_korean'],"투자 예산 (헤알)": investment_amount, "예상 신규 고객 (명)": investment_amount / CAC, "예상 충성 고객 (명)": (investment_amount / CAC) * category_data['conversion_rate'], "예상 총 LTV (헤알)": (investment_amount / CAC) * category_data['avg_ltv'], "예상 ROI (%)": ((investment_amount / CAC) * category_data['avg_ltv'] - investment_amount) / investment_amount * 100}
    return result

# --- 3. Streamlit UI 구성 ---
st.set_page_config(layout="wide")
st.title('Olist: 데이터 기반 마케팅 전략 대시보드 🚀')

tab1, tab2, tab3 = st.tabs(["**1. 포트폴리오 비교 시뮬레이터**", "**2. 예측 모델 기반 전략 시뮬레이터**", "**3. 브라질 전체 고객 분석**"])

# --- Tab 1: 포트폴리오 비교 시뮬레이터 ---
with tab1:
    st.markdown("비교하고 싶은 **'관문 상품' 카테고리들을 선택**하고, **각각의 마케팅 예산을 다르게 설정**하여 최적의 투자 포트폴리오를 찾아보세요.")
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.subheader('⚙️ 시뮬레이션 설정')
        korean_categories_sorted = sorted(final_kpi_table['product_category_name_korean'].unique())
        selected_categories = st.multiselect('1. 비교할 카테고리를 선택하세요 (최대 3개):', korean_categories_sorted, default=['건강/미용', '컴퓨터', '스포츠/레저'])
        if len(selected_categories) > 3:
            st.warning('최대 3개의 카테고리만 선택할 수 있습니다.'); selected_categories = selected_categories[:3]
        budgets = {}
        if selected_categories:
            st.markdown("---"); st.write('**2. 카테고리별 예산을 설정하세요:**')
            for category in selected_categories:
                budgets[category] = st.number_input(f"'{category}' 예산 (헤알, BRL)", 10000, 1000000, 100000, 10000, key=f"budget_{category}")
    with col2:
        st.subheader('📊 시뮬레이션 결과 비교')
        if not selected_categories:
            st.info('왼쪽 설정 창에서 비교할 카테고리를 1개 이상 선택해주세요.')
        else:
            results_list = []
            for korean_name, budget in budgets.items():
                english_name = final_kpi_table[final_kpi_table['product_category_name_korean'] == korean_name]['product_category_name_english'].iloc[0]
                results_list.append(marketing_investment_simulator(english_name, budget, final_kpi_table))
            results_df = pd.DataFrame(results_list)
            st.write("**종합 결과표**"); st.dataframe(results_df.style.format({"투자 예산 (헤알)": "R${:,.0f}", "예상 신규 고객 (명)": "{:,.0f}", "예상 충성 고객 (명)": "{:,.1f}", "예상 총 LTV (헤알)": "R${:,.0f}", "예상 ROI (%)": "{:.1f}%"}))
            st.write("**핵심 성과 지표(KPI) 비교 그래프**")
            fig1 = px.bar(results_df, x='투자 카테고리', y='예상 충성 고객 (명)', title='예상 충성 고객 수 비교', text_auto='.1f'); st.plotly_chart(fig1, use_container_width=True)
            fig2 = px.bar(results_df, x='투자 카테고리', y='예상 ROI (%)', title='예상 투자수익률(ROI) 비교', text_auto='.1f'); st.plotly_chart(fig2, use_container_width=True)

# --- Tab 2: 예측 모델 기반 전략 시뮬레이터 ---
with tab2:
    st.markdown("카테고리와 예산을 선택하여, **머신러닝 모델이 예측하는** 투자 효과를 **Before & After 지도**로 확인해보세요.")
    
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        korean_categories_sorted_tab2 = sorted(final_kpi_table['product_category_name_korean'].unique())
        selected_category_korean_tab2 = st.selectbox('1. 예측할 카테고리를 선택하세요:', korean_categories_sorted_tab2, index=korean_categories_sorted_tab2.index('건강/미용'))
    with sim_col2:
        investment_budget_tab2 = st.slider('2. 마케팅 예산을 설정하세요 (헤알, BRL):', 10000, 1000000, 100000, 10000)
    
    selected_category_english = final_kpi_table[final_kpi_table['product_category_name_korean'] == selected_category_korean_tab2]['product_category_name_english'].iloc[0]
    
    # ★★★ 'Before' 지도를 선택한 카테고리 기준으로 필터링 ★★★
    before_df = category_state_loyal_customers[category_state_loyal_customers['product_category_name_english'] == selected_category_english]
    
    CAC = 30; total_new_customers = investment_budget_tab2 / CAC
    dist_weights = cat_state_dist[cat_state_dist['product_category_name_english'] == selected_category_english]
    
    after_df = pd.merge(before_df, dist_weights, on='customer_state', how='outer', suffixes=('', '_dist')).fillna(0)
    after_df = pd.merge(after_df, model_predictions[model_predictions['product_category_name_english'] == selected_category_english], on='customer_state', how='outer').fillna(0)
    
    after_df['new_loyal_customers'] = (total_new_customers * after_df['state_weight']) * after_df['predicted_conversion_rate']
    after_df['loyal_customers_after'] = after_df['loyal_customers'] + after_df['new_loyal_customers']

    map_col1, map_col2 = st.columns(2)
    min_val = 0
    max_val = after_df['loyal_customers_after'].max()
    
    with map_col1:
        fig_before = px.choropleth(before_df, geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson", locations='customer_state', featureidkey="properties.sigla", color='loyal_customers', color_continuous_scale="Blues", range_color=(min_val, max_val), scope="south america", hover_name='customer_state', hover_data={'loyal_customers': ':.0f'})
        fig_before.update_layout(title_text=f"BEFORE: '{selected_category_korean_tab2}' 충성 고객 분포", margin={"r":0,"t":40,"l":0,"b":0}); st.plotly_chart(fig_before, use_container_width=True)
    with map_col2:
        fig_after = px.choropleth(after_df, geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson", locations='customer_state', featureidkey="properties.sigla", color='loyal_customers_after', color_continuous_scale="Blues", range_color=(min_val, max_val), scope="south america", hover_name='customer_state', hover_data={'loyal_customers_after': ':.1f'})
        fig_after.update_layout(title_text=f"AFTER: '{selected_category_korean_tab2}' 투자 후 예측", margin={"r":0,"t":40,"l":0,"b":0}); st.plotly_chart(fig_after, use_container_width=True)

# --- Tab 3: 브라질 전체 고객 분석 ---
with tab3:
    st.subheader("브라질 주(State)별 전체 고객 데이터 분석")
    map_metric = st.radio("지도에 표시할 지표를 선택하세요:", ('총 고객 수', '평균 LTV', '재구매 전환율'), horizontal=True, key="total_map_radio")
    metric_mapping = {'총 고객 수': ('total_customers', 'Blues'), '평균 LTV': ('avg_ltv', 'Greens'), '재구매 전환율': ('conversion_rate', 'Reds')}
    selected_column, color_scale = metric_mapping[map_metric]
    
    fig_map_total = px.choropleth(state_kpi_data, geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson", locations='customer_state', featureidkey="properties.sigla", color=selected_column, color_continuous_scale=color_scale, scope="south america", hover_name='customer_state', hover_data={'total_customers': ':,', 'avg_ltv': ':,.2f', 'conversion_rate': ':.2%'})
    fig_map_total.update_geos(fitbounds="locations", visible=False); fig_map_total.update_layout(title_text=f'브라질 주(State)별 {map_metric} 분포', margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_map_total, use_container_width=True)
import streamlit as st
from FortniteReplayReader import ReplayReader

st.title("Fortnite リプレイポイント集計ツール")

# ポイント設定
rank_point = st.number_input("順位ごとのポイント（例: 1位=100, 2位=80...）", min_value=0, value=100)
kill_point = st.number_input("キル数ごとのポイント", min_value=0, value=50)
damage_point = st.number_input("与ダメージごとのポイント（1ダメージあたり）", min_value=0.0, value=0.5)

uploaded_file = st.file_uploader("リプレイファイルをアップロード（.replay）", type=["replay"])

if uploaded_file:
    # ファイル保存
    with open("temp.replay", "wb") as f:
        f.write(uploaded_file.read())
    replay = ReplayReader("temp.replay")

    # 仮のデータ構造
    players = []
    for player in replay.players:
        # 仮: プレイヤーデータ取得例
        name = player.name
        rank = player.rank
        kills = player.kills
        damage = player.damage_dealt

        # ポイント計算
        point = (rank_point * (1 if rank == 1 else 0)) + (kill_point * kills) + (damage_point * damage)
        players.append({
            "name": name,
            "rank": rank,
            "kills": kills,
            "damage": damage,
            "point": point
        })
    
    # ポイント順でソート
    players = sorted(players, key=lambda x: x["point"], reverse=True)
    
    st.write("### 集計結果（ポイント順）")
    st.table([
        {"順位": i+1, "名前": p["name"], "キル数": p["kills"], "与ダメージ": int(p["damage"]), "ポイント": int(p["point"])}
        for i, p in enumerate(players)
    ])

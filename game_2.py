import streamlit as st
import pandas as pd
import time
import json

# Page config for mobile optimization
st.set_page_config(
    page_title="♠️ Spade Game Score Count",
    page_icon="♠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark poker theme with mobile optimization
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit branding for cleaner mobile view */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title styling with animation */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(45deg, #FFD700, #FF0000, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        animation: glow 2s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
    }
    
    @keyframes glow {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Card suit animations */
    .card-suits {
        font-size: 40px;
        text-align: center;
        margin: 15px 0;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .suit-spade { 
        color: #FFD700; 
        animation-delay: 0s;
        display: inline-block;
        margin: 0 8px;
    }
    .suit-heart { 
        color: #FF0000; 
        animation-delay: 0.5s;
        display: inline-block;
        margin: 0 8px;
    }
    .suit-diamond { 
        color: #FF0000; 
        animation-delay: 1s;
        display: inline-block;
        margin: 0 8px;
    }
    .suit-club { 
        color: #FFD700; 
        animation-delay: 1.5s;
        display: inline-block;
        margin: 0 8px;
    }
    
    /* Round indicator with pulse */
    .round-indicator {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        padding: 12px 25px;
        border-radius: 50px;
        font-size: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 15px auto;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4); }
        50% { box-shadow: 0 5px 30px rgba(255, 215, 0, 0.6); }
        100% { box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4); }
    }
    
    /* Player cards styling */
    .player-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 15px;
        padding: 15px;
        margin: 8px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 2px solid #FFD700;
        transition: transform 0.3s;
    }
    
    .player-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.3);
        border-color: #FF0000;
    }
    
    /* Score display */
    .score-display {
        font-size: 32px;
        font-weight: 700;
        color: #FFD700;
        text-align: center;
        margin: 8px 0;
        text-shadow: 2px 2px 4px rgba(255, 0, 0, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF0000 0%, #8B0000 100%);
        color: white;
        border: 2px solid #FFD700;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.4);
        width: 100%;
        height: 45px;
        margin: 3px 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #FFD700;
        border: 2px solid #FFD700;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: #1a1a1a !important;
        color: #FFD700 !important;
        border-radius: 10px;
    }
    
    /* Mobile specific optimizations */
    @media (max-width: 768px) {
        .main-title {
            font-size: 28px;
        }
        .card-suits {
            font-size: 30px;
        }
        .stButton > button {
            height: 40px;
            font-size: 12px;
            padding: 8px 12px;
        }
        .score-display {
            font-size: 28px;
        }
        .round-indicator {
            font-size: 18px;
            padding: 10px 20px;
        }
        .player-card {
            padding: 12px;
            margin: 5px 0;
        }
    }
    
    /* Fix for mobile viewport */
    @media screen and (max-width: 768px) {
        .block-container {
            padding: 1rem 0.5rem !important;
        }
    }
    
    /* Winner animation */
    .winner-announcement {
        font-size: 28px;
        font-weight: 700;
        color: #FFD700;
        text-align: center;
        animation: bounce 1s infinite;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Trophy emoji animation */
    .trophy {
        font-size: 60px;
        animation: spin 2s linear infinite;
        display: inline-block;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize or load session state with persistence
def load_state():
    """Load state from browser storage or initialize new state"""
    if 'game_loaded' not in st.session_state:
        st.session_state.game_loaded = True
        st.session_state.game_started = False
        st.session_state.num_players = 4
        st.session_state.player_names = []
        st.session_state.current_round = 1
        st.session_state.scores = {}
        st.session_state.round_scores = {}
        st.session_state.total_scores = {}
        st.session_state.show_celebration = False
        st.session_state.last_save_time = time.time()

def save_state():
    """Save current state to maintain persistence"""
    st.session_state.last_save_time = time.time()
    # Streamlit automatically persists session state between reruns

# Load state on startup
load_state()

# Auto-save mechanism
if 'last_save_time' in st.session_state:
    if time.time() - st.session_state.last_save_time > 5:  # Auto-save every 5 seconds
        save_state()

def reset_game():
    if st.button("⚠️ Confirm Reset", type="secondary"):
        st.session_state.game_started = False
        st.session_state.player_names = []
        st.session_state.current_round = 1
        st.session_state.scores = {}
        st.session_state.round_scores = {}
        st.session_state.total_scores = {}
        st.session_state.show_celebration = False
        save_state()
        st.rerun()
    if st.button("Cancel", type="primary"):
        st.rerun()

def start_game(num_players, names):
    st.session_state.num_players = num_players
    st.session_state.player_names = names
    st.session_state.game_started = True
    st.session_state.current_round = 1
    
    # Initialize scores
    for name in names:
        st.session_state.scores[name] = []
        st.session_state.round_scores[name] = 0
        st.session_state.total_scores[name] = 0
    save_state()

def update_round_score(player, delta):
    st.session_state.round_scores[player] += delta
    save_state()

def save_round():
    # Save current round scores
    for player in st.session_state.player_names:
        st.session_state.scores[player].append(st.session_state.round_scores[player])
        st.session_state.total_scores[player] += st.session_state.round_scores[player]
        st.session_state.round_scores[player] = 0
    
    # Move to next round
    if st.session_state.current_round < 13:
        st.session_state.current_round += 1
    else:
        st.session_state.game_ended = True
        st.session_state.show_celebration = True
    save_state()

# Main app header with animations
st.markdown('<h1 class="main-title">♠️ SPADE GAME SCORE COUNT ♠️</h1>', unsafe_allow_html=True)
st.markdown('''<div class="card-suits">
    <span class="suit-spade">♠️</span>
    <span class="suit-heart">♥️</span>
    <span class="suit-diamond">♦️</span>
    <span class="suit-club">♣️</span>
</div>''', unsafe_allow_html=True)

if not st.session_state.game_started:
    # Game setup with fun UI
    st.markdown("### 🎮 Let's Start a New Game!")
    st.markdown("---")
    
    # Select number of players with visual feedback
    st.markdown("#### 👥 Select Number of Players")
    
    cols = st.columns(2)
    with cols[0]:
        if st.button("🎯 4 Players", use_container_width=True, type="primary"):
            st.session_state.num_players = 4
            st.balloons()
    with cols[1]:
        if st.button("🎯 8 Players", use_container_width=True, type="primary"):
            st.session_state.num_players = 8
            st.balloons()
    
    if st.session_state.num_players:
        st.markdown(f"### ✅ Selected: {st.session_state.num_players} Players")
        st.markdown("---")
        
        # Enter player names with emojis
        st.markdown("### 📝 Enter Player Names")
        names = []
        
        player_emojis = ["👑", "🎯", "⭐", "🏆", "💎", "🎪", "🎨", "🎭"]
        
        # Responsive columns for mobile
        cols = st.columns(2 if st.session_state.num_players <= 4 else 2)
        for i in range(st.session_state.num_players):
            with cols[i % 2]:
                name = st.text_input(
                    f"{player_emojis[i]} Player {i+1}", 
                    key=f"name_{i}",
                    placeholder=f"Enter name..."
                )
                if name:
                    names.append(name)
        
        # Start game button
        if st.button("🚀 START GAME 🚀", type="primary", use_container_width=True):
            if len(names) == st.session_state.num_players and all(names):
                start_game(st.session_state.num_players, names)
                st.balloons()
                st.success("🎉 Game Started! Let's Play!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"⚠️ Please enter all {st.session_state.num_players} player names")

else:
    # Game in progress with enhanced UI
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="round-indicator">🎲 Round {st.session_state.current_round} of 13 🎲</div>', 
                   unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Reset", type="secondary", use_container_width=True):
            st.warning("Are you sure you want to reset the game?")
            reset_game()
    
    st.markdown("---")
    
    # Score input section with player cards - Mobile optimized
    st.markdown("### 🎯 Score This Round")
    
    # Responsive layout for mobile
    num_cols = 2 if st.session_state.num_players <= 4 else 2
    cols = st.columns(num_cols)
    
    for i, player in enumerate(st.session_state.player_names):
        with cols[i % num_cols]:
            # Player card with gradient border
            st.markdown(f"""
                <div class="player-card">
                    <h4 style="text-align: center; color: #FFD700; margin: 5px;">♠️ {player} ♠️</h4>
                    <div class="score-display">{st.session_state.round_scores[player]}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Score adjustment buttons - Compact for mobile
            button_cols = st.columns(4)
            with button_cols[0]:
                if st.button("−10", key=f"minus10_{player}_{st.session_state.current_round}", use_container_width=True):
                    update_round_score(player, -10)
                    st.rerun()
            with button_cols[1]:
                if st.button("−1", key=f"minus1_{player}_{st.session_state.current_round}", use_container_width=True):
                    update_round_score(player, -1)
                    st.rerun()
            with button_cols[2]:
                if st.button("+1", key=f"plus1_{player}_{st.session_state.current_round}", use_container_width=True):
                    update_round_score(player, 1)
                    st.rerun()
            with button_cols[3]:
                if st.button("+10", key=f"plus10_{player}_{st.session_state.current_round}", use_container_width=True):
                    update_round_score(player, 10)
                    st.rerun()
    
    st.markdown("---")
    
    # Save round button
    if st.button("💾 SAVE ROUND & CONTINUE ▶️", type="primary", use_container_width=True):
        save_round()
        if st.session_state.current_round <= 13:
            st.success(f"✅ Round {st.session_state.current_round - 1} Saved!")
            st.balloons()
            time.sleep(0.5)
            st.rerun()
    
    # Display running totals with style
    if any(st.session_state.scores.values()):
        st.markdown("---")
        st.markdown("### 📊 Score Board")
        
        # Create styled leaderboard
        leaderboard = []
        for player in st.session_state.player_names:
            player_data = {
                "🏆 Player": player,
                "💰 Total": st.session_state.total_scores[player],
                "📈 Rounds": len(st.session_state.scores[player])
            }
            leaderboard.append(player_data)
        
        # Sort by total score
        leaderboard = sorted(leaderboard, key=lambda x: x["💰 Total"], reverse=True)
        
        # Display leaderboard with medals
        for i, player_data in enumerate(leaderboard):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🎯"
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a1a, #2d2d2d); 
                            padding: 10px; border-radius: 10px; margin: 5px 0; 
                            border: 1px solid #FFD700;">
                    <strong style="color: #FFD700;">{medal} {player_data["🏆 Player"]}</strong>: 
                    <span style="color: #FFD700; font-size: 20px; font-weight: bold;">
                        {player_data["💰 Total"]} pts
                    </span>
                    <span style="color: #999; font-size: 14px;">
                        ({player_data["📈 Rounds"]} rounds)
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        # Detailed score history with EDIT option
        with st.expander("📜 View Detailed Score History", expanded=False):
            # Check if there are any scores to display
            has_scores = any(len(scores) > 0 for scores in st.session_state.scores.values())
            
            if has_scores:
                # Create the data for display
                data_rows = []
                for player in st.session_state.player_names:
                    row = {"Player": player}
                    player_scores = st.session_state.scores.get(player, [])
                    for i, score in enumerate(player_scores):
                        row[f"R{i+1}"] = score
                    row["Total"] = st.session_state.total_scores.get(player, 0)
                    data_rows.append(row)
                
                # Create and display dataframe
                if data_rows:
                    df = pd.DataFrame(data_rows)
                    # Fill NaN values with "-" for better display
                    df = df.fillna("-")
                    st.dataframe(
                        df, 
                        use_container_width=True, 
                        hide_index=True
                    )
                    
                    # Also show as simple text for mobile compatibility
                    st.markdown("#### 📱 Mobile View:")
                    for player in st.session_state.player_names:
                        scores_text = ", ".join([str(s) for s in st.session_state.scores[player]])
                        total = st.session_state.total_scores[player]
                        st.markdown(f"**{player}**: {scores_text} | **Total: {total}**")
            else:
                st.info("No completed rounds yet. Play and save a round to see history!")
        
        # Edit Previous Rounds Section
        with st.expander("✏️ Edit Previous Round Scores", expanded=False):
            has_scores = any(len(scores) > 0 for scores in st.session_state.scores.values())
            
            if has_scores:
                # Select round to edit
                completed_rounds = len(st.session_state.scores[st.session_state.player_names[0]])
                if completed_rounds > 0:
                    round_to_edit = st.selectbox(
                        "Select Round to Edit",
                        options=list(range(1, completed_rounds + 1)),
                        format_func=lambda x: f"Round {x}",
                        key="edit_round_select"
                    )
                    
                    st.markdown(f"### 📝 Editing Round {round_to_edit}")
                    
                    # Create columns for editing scores
                    edit_cols = st.columns(2 if st.session_state.num_players <= 4 else 2)
                    new_scores = {}
                    
                    for i, player in enumerate(st.session_state.player_names):
                        with edit_cols[i % 2]:
                            current_score = st.session_state.scores[player][round_to_edit - 1]
                            new_score = st.number_input(
                                f"🎯 {player}",
                                value=current_score,
                                key=f"edit_{player}_{round_to_edit}",
                                step=1
                            )
                            new_scores[player] = new_score
                            
                            # Show difference if changed
                            if new_score != current_score:
                                diff = new_score - current_score
                                color = "#27AE60" if diff > 0 else "#E74C3C"
                                st.markdown(f"<span style='color: {color};'>Change: {diff:+d}</span>", 
                                          unsafe_allow_html=True)
                    
                    # Save edited scores button
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Save Changes", type="primary", use_container_width=True):
                            # Update scores and recalculate totals
                            for player in st.session_state.player_names:
                                old_score = st.session_state.scores[player][round_to_edit - 1]
                                new_score = new_scores[player]
                                
                                # Update the score for that round
                                st.session_state.scores[player][round_to_edit - 1] = new_score
                                
                                # Recalculate total
                                st.session_state.total_scores[player] = sum(st.session_state.scores[player])
                            
                            save_state()
                            st.success(f"✅ Round {round_to_edit} scores updated!")
                            time.sleep(0.5)
                            st.rerun()
                    
                    with col2:
                        if st.button("❌ Cancel", type="secondary", use_container_width=True):
                            st.rerun()
            else:
                st.info("No completed rounds to edit yet.")
        
        # Check if game is over
        if st.session_state.current_round > 13:
            st.markdown("---")
            st.markdown('<div class="trophy">🏆</div>', unsafe_allow_html=True)
            st.markdown('<h1 class="winner-announcement">🎊 GAME COMPLETE! 🎊</h1>', unsafe_allow_html=True)
            
            # Final scores with celebration
            sorted_players = sorted(st.session_state.player_names, 
                                  key=lambda x: st.session_state.total_scores[x], 
                                  reverse=True)
            
            # Winner announcement
            winner = sorted_players[0]
            winner_score = st.session_state.total_scores[winner]
            
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFD700, #FFA500); 
                            padding: 20px; border-radius: 20px; text-align: center; 
                            margin: 20px 0; box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);">
                    <h2 style="color: #000; margin: 0;">👑 CHAMPION 👑</h2>
                    <h1 style="color: #000; margin: 10px 0;">{winner}</h1>
                    <h3 style="color: #000; margin: 0;">Score: {winner_score} points</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Final leaderboard
            st.markdown("### 🏅 Final Leaderboard")
            for i, player in enumerate(sorted_players, 1):
                score = st.session_state.total_scores[player]
                if i == 1:
                    st.markdown(f"### 🥇 **{player}**: {score} points 👑")
                elif i == 2:
                    st.markdown(f"### 🥈 **{player}**: {score} points")
                elif i == 3:
                    st.markdown(f"### 🥉 **{player}**: {score} points")
                else:
                    st.markdown(f"### 🎯 {i}. **{player}**: {score} points")
            
            # Celebration effects
            if st.session_state.show_celebration:
                st.balloons()
                st.snow()
                st.session_state.show_celebration = False

# Footer with style
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #FFD700; opacity: 0.8; padding: 15px;">
        <p>♠️ ♥️ ♦️ ♣️ Spade Game Score Counter ♣️ ♦️ ♥️ ♠️</p>
        <p style="font-size: 12px;">Made with ❤️ for Card Game Lovers</p>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd

# Page config for mobile optimization
st.set_page_config(
    page_title="Card Game Score Tracker",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile optimization
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        margin: 2px;
    }
    .score-button {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
    }
    div[data-testid="column"] {
        padding: 2px;
    }
    .round-header {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
        margin: 20px 0;
    }
    @media (max-width: 768px) {
        .stButton > button {
            height: 45px;
            font-size: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.num_players = 4
    st.session_state.player_names = []
    st.session_state.current_round = 1
    st.session_state.scores = {}
    st.session_state.round_scores = {}
    st.session_state.total_scores = {}

def reset_game():
    st.session_state.game_started = False
    st.session_state.player_names = []
    st.session_state.current_round = 1
    st.session_state.scores = {}
    st.session_state.round_scores = {}
    st.session_state.total_scores = {}

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

def update_round_score(player, delta):
    st.session_state.round_scores[player] += delta

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

# Main app
st.title("🎴 Card Game Score Tracker")

if not st.session_state.game_started:
    # Game setup
    st.header("Game Setup")
    
    # Select number of players
    col1, col2 = st.columns(2)
    with col1:
        if st.button("4 Players", use_container_width=True, type="primary"):
            st.session_state.num_players = 4
    with col2:
        if st.button("8 Players", use_container_width=True, type="primary"):
            st.session_state.num_players = 8
    
    st.subheader(f"Selected: {st.session_state.num_players} Players")
    
    # Enter player names
    st.subheader("Enter Player Names")
    names = []
    
    # Create columns for better mobile layout
    if st.session_state.num_players == 4:
        cols = st.columns(2)
        for i in range(4):
            with cols[i % 2]:
                name = st.text_input(f"Player {i+1}", key=f"name_{i}")
                if name:
                    names.append(name)
    else:
        cols = st.columns(2)
        for i in range(8):
            with cols[i % 2]:
                name = st.text_input(f"Player {i+1}", key=f"name_{i}")
                if name:
                    names.append(name)
    
    # Start game button
    if st.button("Start Game", type="primary", use_container_width=True):
        if len(names) == st.session_state.num_players and all(names):
            start_game(st.session_state.num_players, names)
            st.rerun()
        else:
            st.error(f"Please enter all {st.session_state.num_players} player names")

else:
    # Game in progress
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f'<div class="round-header">Round {st.session_state.current_round} of 13</div>', 
                   unsafe_allow_html=True)
    with col3:
        if st.button("Reset Game", type="secondary"):
            reset_game()
            st.rerun()
    
    # Score input section
    st.subheader("Enter Scores for This Round")
    
    # Display players in grid layout for better mobile experience
    if st.session_state.num_players == 4:
        cols = st.columns(2)
        for i, player in enumerate(st.session_state.player_names):
            with cols[i % 2]:
                st.markdown(f"**{player}**")
                st.markdown(f"Current: **{st.session_state.round_scores[player]}**")
                
                # Score adjustment buttons
                button_cols = st.columns(4)
                with button_cols[0]:
                    if st.button("-10", key=f"minus10_{player}_{st.session_state.current_round}"):
                        update_round_score(player, -10)
                        st.rerun()
                with button_cols[1]:
                    if st.button("-1", key=f"minus1_{player}_{st.session_state.current_round}"):
                        update_round_score(player, -1)
                        st.rerun()
                with button_cols[2]:
                    if st.button("+1", key=f"plus1_{player}_{st.session_state.current_round}"):
                        update_round_score(player, 1)
                        st.rerun()
                with button_cols[3]:
                    if st.button("+10", key=f"plus10_{player}_{st.session_state.current_round}"):
                        update_round_score(player, 10)
                        st.rerun()
                
                st.markdown("---")
    else:
        cols = st.columns(2)
        for i, player in enumerate(st.session_state.player_names):
            with cols[i % 2]:
                st.markdown(f"**{player}**")
                st.markdown(f"Current: **{st.session_state.round_scores[player]}**")
                
                # Score adjustment buttons
                button_cols = st.columns(4)
                with button_cols[0]:
                    if st.button("-10", key=f"minus10_{player}_{st.session_state.current_round}"):
                        update_round_score(player, -10)
                        st.rerun()
                with button_cols[1]:
                    if st.button("-1", key=f"minus1_{player}_{st.session_state.current_round}"):
                        update_round_score(player, -1)
                        st.rerun()
                with button_cols[2]:
                    if st.button("+1", key=f"plus1_{player}_{st.session_state.current_round}"):
                        update_round_score(player, 1)
                        st.rerun()
                with button_cols[3]:
                    if st.button("+10", key=f"plus10_{player}_{st.session_state.current_round}"):
                        update_round_score(player, 10)
                        st.rerun()
                
                st.markdown("---")
    
    # Save round button
    if st.button("Save Round & Continue", type="primary", use_container_width=True):
        save_round()
        if st.session_state.current_round <= 13:
            st.rerun()
    
    # Display running totals
    if any(st.session_state.scores.values()):
        st.subheader("Running Totals")
        
        # Create a simple display without dataframe
        # Show scores in a more reliable way
        for player in st.session_state.player_names:
            player_scores = st.session_state.scores[player]
            total = st.session_state.total_scores[player]
            
            # Display player name and total
            st.markdown(f"**{player}** - Total: **{total}**")
            
            # Display round scores
            if player_scores:
                rounds_text = " | ".join([f"R{i+1}: {score}" for i, score in enumerate(player_scores)])
                st.text(rounds_text)
            st.markdown("---")
        
        # Check if game is over
        if st.session_state.current_round > 13:
            st.success("🎉 Game Complete!")
            st.subheader("Final Scores")
            
            # Sort players by total score
            sorted_players = sorted(st.session_state.player_names, 
                                  key=lambda x: st.session_state.total_scores[x], 
                                  reverse=True)
            
            for i, player in enumerate(sorted_players, 1):
                score = st.session_state.total_scores[player]
                if i == 1:
                    st.markdown(f"🥇 **{player}**: {score} points")
                elif i == 2:
                    st.markdown(f"🥈 **{player}**: {score} points")
                elif i == 3:
                    st.markdown(f"🥉 **{player}**: {score} points")
                else:
                    st.markdown(f"{i}. **{player}**: {score} points")

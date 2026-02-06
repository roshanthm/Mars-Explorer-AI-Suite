import streamlit as st
import random
import streamlit.components.v1 as components
import time

def load_mars_facts():
    return [
        "Mars has the largest volcano in the solar system, Olympus Mons.",
        "Mars has two moons: Phobos and Deimos.",
        "A year on Mars is 687 Earth days long.",
        "Mars' atmosphere is 95% carbon dioxide.",
        "Mars has the largest dust storms in the solar system.",
        "The average temperature on Mars is about -63°C (-82°F).",
        "Mars' gravity is about 38% of Earth's.",
        "Sunsets on Mars appear blue due to the way dust scatters light.",
        "Mars has seasons like Earth because both planets are tilted on their axes.",
        "The highest mountain on Mars is three times taller than Mount Everest."
    ]

def main():
    st.title("Mars Information Center")
    
    # Tabs for different categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Geography", "Missions", "Research", "Blog"])
    
    with tab1:
        st.header("About Mars")
        st.write("""
        Mars, often called the Red Planet, is the fourth planet from the Sun in our solar system. 
        It has captured human imagination for centuries and is a prime target for space exploration.
        
        The planet's reddish appearance is due to iron oxide (rust) on its surface. Mars has many 
        Earth-like features including polar ice caps, seasons, and a day length similar to Earth's.
        """)
        
        # Did You Know widget
        with st.expander("Did You Know? (Click to reveal a random fact)"):
            fact = random.choice(load_mars_facts())
            st.info(fact)
    
    with tab2:
        st.header("Martian Geography")
        st.write("""
        Mars features some of the most dramatic landscapes in the solar system:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Major Features")
            st.write("""
            - **Olympus Mons**: The largest volcano in the solar system
            - **Valles Marineris**: A canyon system as long as the United States
            - **Polar Ice Caps**: Composed of water ice and dry ice
            - **Impact Craters**: Including the massive Hellas Basin
            """)
            
        with col2:
            # Define image data
            mars_features = {
                "Olympus Mons - Largest Volcano": "https://vajiram-prod.s3.ap-south-1.amazonaws.com/Olympus_Mons_efbfff8fb1.webp",
                "Valles Marineris - Canyon System": "https://upload.wikimedia.org/wikipedia/commons/5/56/Mars_Valles_Marineris.jpeg",
                "Polar Ice Caps": "https://d2pn8kiwq2w21t.cloudfront.net/original_images/jpegPIA13163.jpg",
                "Impact Craters": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_0JxyfKsFlvdAf6k7grmk0-gzW7LfTQDcKw&s"
            }

            # Initialize session states if they don't exist
            if 'current_image_index' not in st.session_state:
                st.session_state.current_image_index = 0
            if 'last_update_time' not in st.session_state:
                st.session_state.last_update_time = time.time()

            # Get list of captions and URLs
            captions = list(mars_features.keys())
            urls = list(mars_features.values())

            # Check if 4 seconds have passed
            current_time = time.time()
            if current_time - st.session_state.last_update_time >= 4:
                st.session_state.current_image_index = (st.session_state.current_image_index + 1) % len(mars_features)
                st.session_state.last_update_time = current_time
                st.rerun()

            # Display current image
            try:
                st.image(
                    urls[st.session_state.current_image_index],
                    caption=captions[st.session_state.current_image_index],
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")

            # Add image counter and manual controls
            col_left, col_center, col_right = st.columns([2, 6, 2])
            
            with col_left:
                if st.button("←"):
                    st.session_state.current_image_index = (st.session_state.current_image_index - 1) % len(mars_features)
                    st.session_state.last_update_time = current_time
                    st.rerun()
            
            # with col_center:
            #     st.caption(f"Image {st.session_state.current_image_index + 1} of {len(mars_features)}")
            
            with col_right:
                if st.button("→"):
                    st.session_state.current_image_index = (st.session_state.current_image_index + 1) % len(mars_features)
                    st.session_state.last_update_time = current_time
                    st.rerun()
    
    with tab3:
        st.header("Mars Missions")
        st.write("""
        Numerous missions have been sent to Mars, including rovers, landers, and orbiters.
        Here are some of the most significant ongoing missions:
        """)
        
        # Mission timeline
        with st.expander("Active Missions"):
            st.write("🚀 **Perseverance Rover (2020-present)**")
            st.write("- Searching for signs of ancient microbial life")
            st.write("- Collecting rock and soil samples")
            st.write("- Testing oxygen production from Mars atmosphere")
            
            st.write("🚀 **Curiosity Rover (2012-present)**")
            st.write("- Studying Mars' climate and geology")
            st.write("- Assessing environmental conditions for microbial life")
            
            st.write("🚀 **InSight Lander (2018-present)**")
            st.write("- Studying Mars' interior structure")
            st.write("- Measuring Marsquakes")
    
    with tab4:
        st.header("Current Research")
        st.write("""
        Scientists are currently focusing on several key areas of Mars research:
        """)
        
        research_areas = {
            "🔬 Search for Life": " This research focuses on identifying signs of past or present life on Mars, exploring the planet's potential to support microbial life. [Investigating potential biosignatures and habitable environments](https://astrobiology.nasa.gov/).",
            
            "🌡 Climate Studies": "This area explores the history of Martian climate and how it may have supported life in the past, as well as its implications for future habitability. \n[Understanding Mars' past and present climate patterns](https://climate.nasa.gov/). ",
            
            "🚀 Human Exploration": "Research is centered on developing the technology and understanding the challenges for sending humans to Mars, ensuring astronaut safety and sustainability during long-duration missions. [Preparing for future human missions to Mars](https://www.nasa.gov/hrp/). ",
            
            "🪨 Geological History": " By studying Mars' surface and rock formations, scientists learn about the planet's past, including volcanic activity, tectonics, and ancient rivers and lakes. [Mapping the planet's geological evolution](https://mars.nasa.gov/). ",
            
            "💧 Water Presence": "This area investigates evidence of past water on Mars, such as ancient riverbeds, lakes, and ice. These findings are essential for understanding past life and future human settlement. More details can be found in the [NASA link on water presence](https://mars.nasa.gov/msp98/science/sc-water.html).",
            
            "🌍 Marsquakes & Seismology": "Researchers analyze Marsquakes to learn more about the planet's interior structure, its geological processes, and the history of its tectonic activity. For more information, visit [NASA's Marsquakes & Seismology page](https://mars.nasa.gov/insight/).",
            
            "🤖 AI & Robotics": "This field applies advanced AI and robotic technologies to enhance the capabilities of Mars rovers and other autonomous systems, improving data collection and decision-making on Mars missions. Learn more on [NASA's AI & Robotics page](https://www.nasa.gov/artificial-intelligence-in-space/)."
        }

        
        for area, link in research_areas.items():
            with st.expander(area):
                st.markdown(link)
    
    with tab5:
        st.header("📰 Mars Blog & News")
        st.write("Stay updated with the latest discoveries and missions related to Mars. As the fourth planet from the Sun, Mars has long fascinated scientists with its potential for life, its geological history, and its future as a destination for human exploration. Below are some of the latest articles and research about Mars:")

        st.markdown("""
        1. **🚀 NASA's Perseverance Rover's Latest Findings**  
        The Perseverance rover has been on Mars since 2021, exploring the Jezero Crater, searching for signs of ancient life, and collecting rock samples for future missions. [Click to read more](https://mars.nasa.gov/mars2020/)
        
        2. **🔭 Is There Water on Mars? Scientists Investigate**  
        Water is essential for life as we know it. Scientists are continuously investigating Mars for signs of ancient rivers, lakes, and underground water that could have supported life in the past. [Click to read more](https://mars.nasa.gov/news/)
        
        3. **🤖 AI in Space: How It's Revolutionizing Exploration**  
        Artificial Intelligence is playing an increasing role in space exploration, helping rovers navigate the Martian surface and analyze data faster and more accurately. [Click to read more](https://www.nasa.gov/artificial-intelligence-in-space/)
        
        4. **🛰️ The Future of Mars Colonization**  
        As humanity looks toward Mars as a possible second home, missions like NASA's Artemis and SpaceX's Starship are paving the way for the first human exploration and eventual colonization. [Click to read more](https://www.nasa.gov/mars-colonization/)
        
        5. **🔬 Scientists Discover New Clues About Martian Soil**  
        Understanding Martian soil is key to determining the planet's past potential for life and its future habitability. Recent research has uncovered new findings about the composition and structure of Martian soil. [Click to read more](https://www.nasa.gov/martian-soil-research/)
        """)


if __name__ == "__main__":
    main()
    
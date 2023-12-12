import streamlit as st
import pandas as pd

# Function to create or load CSV file
def create_or_load_csv():
    try:
        df = pd.read_csv('xmas_list.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Name', 'Item', 'Description', 'Link', 'Claimed By'])
        df.to_csv('xmas_list.csv', index=False)
    return df

# Main function to run the Streamlit app
def main():
    st.title("Christmas Wishlist App")

    # Create or load the CSV file
    df = create_or_load_csv()

    # User enters their name
    user_name = st.text_input("Enter your name:", placeholder="Siddharth")

    # Select mode
    page = st.selectbox("What do you want to do?", ["Create My Wishlist", "Buy For Others"])

    if page == "Create My Wishlist":

        # Add a section for item details
        st.header("Item Details")

        # Text input for item, description, and link
        item = st.text_input("Item Name:", placeholder="Sweater")
        description = st.text_input("Description:", placeholder="Size L")
        link = st.text_input("Link:", placeholder="amazon.com/ugly-xmas-sweater")

        # Submit button
        if st.button("Add Item"):
            # Append the data to the CSV file
            prev_entries = pd.read_csv('xmas_list.csv')
            new_entry = pd.DataFrame([{'Name': user_name, 'Item': item, 'Description': description, 'Link': link, 'Claimed By': None}])
            df = pd.concat([prev_entries, new_entry], ignore_index=True)
            df.to_csv('xmas_list.csv', index=False)
            st.success("Item submitted successfully!")

        # Display the current wishlist
        st.header("Current Wishlist")
        user_wishlist = df[df['Name'] == user_name]
        user_wishlist.insert(0, "Remove", False)
        edited_selection_df = st.data_editor(user_wishlist[["Remove", "Name", "Item", "Description", "Link"]])

        if st.button("Remove Items"):
            df = df.drop(user_wishlist[edited_selection_df["Remove"]].index.to_list())
            df.to_csv('xmas_list.csv', index=False)
            st.success("Item submitted successfully!")
    
    elif page == "Buy For Others":

        try:

            # Get a list of unique names in the DataFrame
            others_names = df['Name'].unique().tolist()
            others_names.remove(user_name)

            # Dropdown for selecting a person
            selected_person = st.selectbox("Select a person to view their list:", others_names)

            # Display the selected person's list
            st.header(f"{selected_person}'s Wishlist")
            selected_person_wishlist = df[df['Name'] == selected_person]
            selected_person_wishlist.insert(0, "Select", False)
            edited_selection_df = st.data_editor(selected_person_wishlist[["Select", "Name", "Item", "Description", "Link", "Claimed By"]])

            col1, col2, blank = st.columns([1, 2, 3])
            if col1.button("Claim Items"):
                selections = selected_person_wishlist[edited_selection_df["Select"]].index.to_list()
                for selection in selections:
                    row = df.iloc[selection]
                    if row['Claimed By'] is None or pd.isna(row['Claimed By']):
                        df.iloc[selection, df.columns.get_loc('Claimed By')] = user_name
                        st.success(f"Successfully claimed {row['Item']} for {row['Name']}.")
                    elif row['Claimed By'] == user_name:
                        st.write("You've already claimed this item.")
                    else:
                        st.error(f"Someone else has already claimed {row['Item']} for {row['Name']}.")
                df.to_csv('xmas_list.csv', index=False)

            if col2.button("Unclaim Items", key=1):
                selections = selected_person_wishlist[edited_selection_df["Select"]].index.to_list()
                for selection in selections:
                    row = df.iloc[selection]
                    if row['Claimed By'] == user_name:
                        df.iloc[selection, df.columns.get_loc('Claimed By')] = None
                        st.success(f"Successfully unclaimed {row['Item']} for {row['Name']}.")
                    else:
                        st.error(f"You hadn't claimed buying {row['Item']} for {row['Name']}.")
                df.to_csv('xmas_list.csv', index=False)
            
            # Complete list of all claimed items
            st.header("My Shopping List")

            # Display the selected person's list
            claimed_items = df[df['Claimed By'] == user_name]
            claimed_items.insert(0, "Select", False)
            shopping_list = st.data_editor(claimed_items[["Select", "Name", "Item", "Description", "Link", "Claimed By"]])

            if st.button("Unclaim Items", key=2):
                selections = claimed_items[shopping_list["Select"]].index.to_list()
                for selection in selections:
                    row = df.iloc[selection]
                    if row['Claimed By'] == user_name:
                        df.iloc[selection, df.columns.get_loc('Claimed By')] = None
                        st.success(f"Successfully unclaimed {row['Item']} for {row['Name']}.")
                    else:
                        st.error(f"You hadn't claimed buying {row['Item']} for {row['Name']}.")
                df.to_csv('xmas_list.csv', index=False)

        except:
            st.error("No one has entered a list. Tell people to use the app!")

if __name__ == "__main__":
    main()
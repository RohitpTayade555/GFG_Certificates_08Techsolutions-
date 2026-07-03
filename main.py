import streamlit as st
import pandas as pd
import requests
import re

st.set_page_config(
    page_title='GFG Campus Body HVPM COET Certificates',
    page_icon='assets/favicon.png',
    layout='wide'
)

st.title("GFG Campus Body HVPM COET Certificate")
st.markdown("---")


@st.cache_data
def load_certificate_data():
    try:
        df = pd.read_csv("certificates.csv")
        return df
    except Exception:
        return pd.DataFrame()


def convert_drive_link_to_urls(drive_link):
    try:
        patterns = [
            r"/file/d/([a-zA-Z0-9-_]+)",
            r"id=([a-zA-Z0-9-_]+)",
            r"/d/([a-zA-Z0-9-_]+)",
        ]

        file_id = None
        for pattern in patterns:
            match = re.search(pattern, drive_link)
            if match:
                file_id = match.group(1)
                break

        if file_id:
            direct_link = f"https://drive.google.com/uc?export=download&id={file_id}"
            # Official embedded viewer link which works cleanly across all browsers
            preview_link = f"https://drive.google.com/file/d/{file_id}/preview"
            return direct_link, preview_link
        else:
            return None, None

    except Exception:
        return None, None


@st.cache_data
def download_pdf_from_drive(direct_link):
    try:
        if not direct_link:
            return None

        response = requests.get(direct_link, allow_redirects=True)

        # SAFETY CHECK: If the downloaded content is HTML (starts with <!doctype), it's a login/error screen!
        if response.status_code == 200 and not response.content.strip().startswith(b"<!doctype"):
            return response.content
        else:
            return None
    except Exception:
        return None


def main():
    df = load_certificate_data()

    if df.empty:
        st.error("No certificate data found. Please check your data file.")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Participants")

        names = df["Name"].dropna().astype(str).tolist()
        name_map = {name.title().strip(): name.strip() for name in names}
        display_names = ["Select your name..."] + sorted(list(name_map.keys()))

        selected_display = st.selectbox(
            "Choose your name from the list:",
            options=display_names,
            index=0,
            help="Select your name to view and download your certificate",
        )

        selected_name = name_map.get(selected_display) if selected_display != "Select your name..." else None

        if selected_name:
            drive_link = df[df["Name"].str.strip() == selected_name]["Drive_Link"].iloc[0]
            direct_link, preview_link = convert_drive_link_to_urls(drive_link)

            st.success(" Certificate located!")
            st.info(f"**Selected:** {selected_name}")

            if st.button("Verify Download File", type="primary"):
                with st.spinner("Downloading file data..."):
                    pdf_content = download_pdf_from_drive(direct_link)

                    if pdf_content:
                        st.session_state["pdf_content"] = pdf_content
                        st.session_state["selected_name"] = selected_name
                        st.session_state["is_html_error"] = False
                        st.success(" File verified successfully!")
                        st.rerun()
                    else:
                        st.session_state["pdf_content"] = None
                        st.session_state["selected_name"] = selected_name
                        st.session_state["is_html_error"] = True


        else:
            if selected_display != "Select your name...":
                st.error("Name not found")
            st.info(" Please select your name from the dropdown first")

            ##########
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center; color: #888888; font-size: 12px;">
                <hr style="border: 0; height: 1px; background: #e0e0e0; margin-bottom: 10px;">
                © 2026 GFG Campus Body HVPM COET . All Rights Reserved.<br>
                Developed with ❤️ by <b>Rohit Tayade & 08Tech Solutions</b>
            </div>
            """, 
            unsafe_allow_html=True
        )
            ##########

    with col2:
        st.subheader("Certificate Preview")

        if selected_name and preview_link:
            # Displays the official Google Drive Preview frame interactively
            st.markdown(
                f'<iframe src="{preview_link}" width="100%" height="600px" style="border: none; border-radius: 8px;"></iframe>',
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # Show download button if data is verified as a true PDF binary
            if (
                st.session_state.get("pdf_content") is not None 
                and st.session_state.get("selected_name") == selected_name
            ):
                st.download_button(
                    label="Save Certificate to Device (PDF)",
                    data=st.session_state["pdf_content"],
                    file_name=f"{selected_name.replace(' ', '_')}_Certificate.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            # If Google threw a sign-in block screen, show a direct button link instead
            elif st.session_state.get("is_html_error", False) and st.session_state.get("selected_name") == selected_name:
                st.markdown(
                    f'<a href="{drive_link}" target="_blank" style="text-decoration: none;"><button style="width: 100%; padding: 10px; background-color: #ff4b4b; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;"> Open & Save via Google Drive Directly</button></a>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
            <div style="
                border: 2px dashed #ccc;
                border-radius: 10px;
                padding: 180px 20px;
                text-align: center;
                background: #f8f9fa;
                margin: 20px 0;
            ">
                <h3 style="color: #666; margin-bottom: 10px;"> Certificate Preview</h3>
                <p style="color: #888; margin: 0;">Select your name to load an interactive view pane</p>
            </div>
            """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()


    # import streamlit as st
# import pandas as pd
# import requests
# import re
# import base64

# st.set_page_config(
#     page_title='GFG Campus Body GCECT Certificates',
#     page_icon='assets/favicon.png',
#     layout='wide'
# )

# st.title("🏆 GFG Campus Body GCECT Certificate")
# st.markdown("---")


# @st.cache_data
# def load_certificate_data():
#     try:
#         df = pd.read_csv("certificates.csv")
#         return df
#     except Exception:
#         return pd.DataFrame()


# def convert_drive_link_to_direct(drive_link):
#     try:
#         patterns = [
#             r"/file/d/([a-zA-Z0-9-_]+)",
#             r"id=([a-zA-Z0-9-_]+)",
#             r"/d/([a-zA-Z0-9-_]+)",
#         ]

#         file_id = None
#         for pattern in patterns:
#             match = re.search(pattern, drive_link)
#             if match:
#                 file_id = match.group(1)
#                 break

#         if file_id:
#             direct_link = f"https://drive.google.com/uc?export=download&id={file_id}"
#             view_link = f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"
#             return direct_link, view_link
#         else:
#             return None, drive_link

#     except Exception:
#         return None, drive_link


# @st.cache_data
# def download_pdf_from_drive(direct_link):
#     try:
#         if not direct_link:
#             return None

#         # Use a session to persist cookies if Google Drive serves a confirmation screen
#         session = requests.Session()
#         response = session.get(direct_link, allow_redirects=True)

#         # Check for Google Drive virus scan confirmation page
#         if "confirm=" in response.url or (response.headers.get("Content-Type", "").startswith("text/html")):
#             # Try to grab confirmation token if present
#             match = re.search(r'confirm=([a-zA-Z0-9-_]+)', response.url)
#             if match:
#                 confirm_token = match.group(1)
#                 response = session.get(f"{direct_link}&confirm={confirm_token}", allow_redirects=True)
#             else:
#                 # Standard fallback token trigger
#                 response = session.get(f"{direct_link}&confirm=t", allow_redirects=True)

#         # Validate that the downloaded file is a real PDF (starts with %PDF)
#         if response.status_code == 200 and response.content.startswith(b"%PDF"):
#             return response.content
#         else:
#             return None

#     except Exception:
#         return None


# def display_pdf_preview(pdf_content):
#     with st.spinner("Loading certificate preview..."):
#         try:
#             base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
#             # Using an <object> tag instead of an <iframe> provides more reliable cross-browser rendering
#             pdf_display = f'<object data="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="100%" height="600px"><p>Your browser cannot preview this PDF inline.</p></object>'
#             st.markdown(pdf_display, unsafe_allow_html=True)
#         except Exception as e:
#             st.error(f"Error displaying PDF preview: {str(e)}")


# def main():
#     df = load_certificate_data()

#     if df.empty:
#         st.error("No certificate data found. Please check your data file.")
#         return

#     col1, col2 = st.columns([1, 2])

#     with col1:
#         st.subheader("📋 Participants")

#         names = df["Name"].dropna().astype(str).tolist()
#         name_map = {name.title().strip(): name.strip() for name in names}
#         display_names = ["Select your name..."] + sorted(list(name_map.keys()))

#         selected_display = st.selectbox(
#             "Choose your name from the list:",
#             options=display_names,
#             index=0,
#             help="Select your name to view and download your certificate",
#         )

#         selected_name = name_map.get(selected_display) if selected_display != "Select your name..." else None

#         if selected_name:
#             drive_link = df[df["Name"].str.strip() == selected_name]["Drive_Link"].iloc[0]
#             direct_link, view_link = convert_drive_link_to_direct(drive_link)

#             st.success("✅ Certificate found!")
#             st.info(f"**Selected:** {selected_name}")

#             if st.button("📩 Get Certificate", type="primary"):
#                 with st.spinner("Downloading certificate..."):
#                     pdf_content = download_pdf_from_drive(direct_link)

#                     if pdf_content:
#                         st.session_state["pdf_content"] = pdf_content
#                         st.session_state["selected_name"] = selected_name
#                         st.session_state["download_failed"] = False
#                         st.success("✅ Certificate downloaded successfully!")
#                         st.rerun()
#                     else:
#                         st.session_state["pdf_content"] = None
#                         st.session_state["selected_name"] = selected_name
#                         st.session_state["download_failed"] = True
#                         st.warning("⚠️ High-security / large file restriction detected by your browser.")
#         else:
#             if selected_display != "Select your name...":
#                 st.error("Name not found")
#             st.info("👆 Please select your name from the dropdown first")

#     with col2:
#         st.subheader("📄 Certificate Preview")

#         # Case 1: Successfully downloaded and verified PDF
#         if (
#             st.session_state.get("pdf_content") is not None
#             and st.session_state.get("selected_name") == selected_name
#         ):
#             display_pdf_preview(st.session_state["pdf_content"])

#             st.markdown("<br>", unsafe_allow_html=True)
#             col1, col2, col3 = st.columns([1, 2, 1])
#             with col2:
#                 st.download_button(
#                     label="📥 Download Certificate as PDF",
#                     data=st.session_state["pdf_content"],
#                     file_name=f"{st.session_state['selected_name'].replace(' ', '_')}_Certificate.pdf",
#                     mime="application/pdf",
#                     type="primary",
#                     use_container_width=True
#                 )

#         # Case 2: Fallback activated because automated download was blocked by Drive
#         elif (
#             st.session_state.get("download_failed", False) 
#             and st.session_state.get("selected_name") == selected_name
#         ):
#             st.markdown(
#                 f"""
#             <div style="
#                 border: 2px dashed #ffc107;
#                 border-radius: 10px;
#                 padding: 100px 20px;
#                 text-align: center;
#                 background: #fff3cd;
#                 margin: 20px 0;
#             ">
#                 <h3 style="color: #856404; margin-bottom: 15px;">🔗 Secure Drive Link Ready</h3>
#                 <p style="color: #856404; margin-bottom: 20px;">Google Drive requires manual confirmation to view this certificate.</p>
#                 <a href="{view_link}" target="_blank" style="
#                     background-color: #ffc107;
#                     color: #000;
#                     padding: 12px 30px;
#                     text-decoration: none;
#                     font-weight: bold;
#                     border-radius: 5px;
#                     box-shadow: 0 2px 5px rgba(0,0,0,0.15);
#                 ">👉 View & Download Certificate Directly</a>
#             </div>
#             """,
#                 unsafe_allow_html=True,
#             )

#         # Case 3: Initial Empty State
#         else:
#             st.markdown(
#                 """
#             <div style="
#                 border: 2px dashed #ccc;
#                 border-radius: 10px;
#                 padding: 180px 20px;
#                 text-align: center;
#                 background: #f8f9fa;
#                 margin: 20px 0;
#             ">
#                 <h3 style="color: #666; margin-bottom: 10px;">🏆 Certificate Preview</h3>
#                 <p style="color: #888; margin: 0;">Select your name and download to preview your certificate here</p>
#             </div>
#             """,
#                 unsafe_allow_html=True,
#             )


# if __name__ == "__main__":
#     main()
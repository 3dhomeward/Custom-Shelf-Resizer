import streamlit as st
import numpy as np
from stl import mesh
import tempfile
import os

st.title("Shelf Customizer: Move Right Plug, Stretch Middle (Y), and Depth (X)")

st.write(
    """
    <b>Upload your shelf STL, set a new width and depth, and download your custom part!</b><br>
    - Left plug region (first 15 mm): stays fixed<br>
    - Right plug region (last 15 mm): moves outward<br>
    - Middle: stretches or shrinks as needed<br>
    - Depth: frontmost 16.3 mm is fixed; rest is stretched/shrunk<br>
    <br>
    <i>For best results, STL must have geometry in the "middle" and defined plug/depth regions.</i>
    """,
    unsafe_allow_html=True,
)

def move_right_plug_and_stretch_middle_and_x(
    stl_mesh,
    x_min, x_max, y_min, y_max,
    plug_length=15.0,
    fixed_x=16.3,
    new_width=None,
    new_depth=None
):
    orig_width = y_max - y_min
    orig_depth = x_max - x_min

    delta_y = new_width - orig_width
    delta_x = new_depth - orig_depth

    left_fixed_end = y_min + plug_length
    right_fixed_start = y_max - plug_length
    old_mid_start = left_fixed_end
    old_mid_end = right_fixed_start
    old_mid_len = old_mid_end - old_mid_start
    new_mid_end = right_fixed_start + delta_y
    new_mid_len = new_mid_end - old_mid_start

    fixed_x_boundary = x_min + fixed_x
    old_x_stretch_len = x_max - fixed_x_boundary
    new_x_stretch_len = x_min + new_depth - fixed_x_boundary

    new_mesh = mesh.Mesh(np.copy(stl_mesh.data))
    count_shifted_y = 0
    count_stretched_y = 0
    count_stretched_x = 0

    for tri in range(new_mesh.vectors.shape[0]):
        for pt in range(3):
            x, y, z = new_mesh.vectors[tri][pt]

            # ---- Y Logic: Move right plug, stretch middle, fix left ----
            if y >= right_fixed_start:
                y_new = y + delta_y
                count_shifted_y += 1
            elif old_mid_start < y < old_mid_end and old_mid_len > 0:
                y_new = old_mid_start + (y - old_mid_start) * (new_mid_len / old_mid_len)
                count_stretched_y += 1
            else:
                y_new = y  # fixed left

            # ---- X Logic: Fixed front, stretch/shrink rear ----
            if x > fixed_x_boundary and old_x_stretch_len > 0:
                x_new = fixed_x_boundary + (x - fixed_x_boundary) * (new_x_stretch_len / old_x_stretch_len)
                count_stretched_x += 1
            else:
                x_new = x

            new_mesh.vectors[tri][pt][0] = x_new
            new_mesh.vectors[tri][pt][1] = y_new
            new_mesh.vectors[tri][pt][2] = z

    return new_mesh, count_shifted_y, count_stretched_y, count_stretched_x

uploaded_file = st.file_uploader("Upload STL", type=["stl"])
plug_length = 15.0  # mm
fixed_x = 16.3  # mm

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmpfile:
        tmpfile.write(uploaded_file.read())
        tmpfile.flush()
        temp_path = tmpfile.name

    shelf_stl = mesh.Mesh.from_file(temp_path)
    x_min, x_max = float(np.min(shelf_stl.x)), float(np.max(shelf_stl.x))
    y_min, y_max = float(np.min(shelf_stl.y)), float(np.max(shelf_stl.y))
    orig_width = y_max - y_min
    orig_depth = x_max - x_min

    st.write(f"Original shelf width: {orig_width:.2f} mm (Y from {y_min:.2f} to {y_max:.2f})")
    st.write(f"Original shelf depth: {orig_depth:.2f} mm (X from {x_min:.2f} to {x_max:.2f})")
    st.write(f"Plug region length (each end, Y): {plug_length} mm")
    st.write(f"Fixed front region (X): {fixed_x} mm")

    min_new_width = orig_width + 1.0  # prevent collapse
    min_new_depth = fixed_x + 1.0
    default_new_width = orig_width + 20
    default_new_depth = orig_depth

    new_width = st.number_input(
        "Enter desired overall shelf width (mm):",
        min_value=min_new_width,
        value=default_new_width,
        step=1.0,
        format="%.2f",
    )
    new_depth = st.number_input(
        "Enter desired shelf depth (front-to-back, mm):",
        min_value=min_new_depth,
        value=default_new_depth,
        step=1.0,
        format="%.2f",
    )

    if st.button("Download Custom STL (Right Plug, Middle, X Depth)"):
        new_mesh, count_shifted_y, count_stretched_y, count_stretched_x = move_right_plug_and_stretch_middle_and_x(
            shelf_stl, x_min, x_max, y_min, y_max,
            plug_length=plug_length, fixed_x=fixed_x,
            new_width=new_width, new_depth=new_depth
        )
        st.write(f"Vertices shifted in right plug (Y): {count_shifted_y}")
        st.write(f"Vertices stretched in middle (Y): {count_stretched_y}")
        st.write(f"Vertices stretched in depth (X): {count_stretched_x}")

        with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmpfile2:
            new_mesh.save(tmpfile2.name)
            tmpfile2.seek(0)
            st.download_button(
                label="Download Resized STL",
                data=tmpfile2.read(),
                file_name=f"custom_shelf_Y{int(new_width)}mm_X{int(new_depth)}mm.stl",
                mime="application/sla",
            )
        os.remove(tmpfile2.name)
    os.remove(temp_path)

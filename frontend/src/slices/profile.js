import { createSlice, createAction } from "@reduxjs/toolkit";

const initialState = {
    visible: false,
};

const profileSlice = createSlice({
    name: "profile",
    initialState,
    reducers: {
        setEditModalVisible(state, action) {
            state.visible = action.payload;
        },
    },
    extraReducers: {},
});
export const { setEditModalVisible } = profileSlice.actions;

export default profileSlice.reducer;

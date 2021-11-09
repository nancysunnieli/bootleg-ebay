import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

import ItemsService from "../services/items.service";

const initialState = {
    items: [],
};

export const getAllItems = createAsyncThunk("items/getAllItems", async (limit, thunkAPI) => {
    console.log("get all items");
    try {
        const data = await ItemsService.getAllItems(limit);
        return data;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

const itemsSlice = createSlice({
    name: "items",
    initialState,
    extraReducers: {
        [getAllItems.fulfilled]: (state, action) => {
            state.items = action.payload;
        },
    },
});

const { reducer } = itemsSlice;
export default reducer;

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

// import ItemsService from "../services/items.service";

const initialState = {};

const itemsSlice = createSlice({
  name: "items",
  initialState,
  extraReducers: {},
});

const { reducer } = itemsSlice;
export default reducer;

import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { toast } from "react-toastify";
import NotifsService from "../services/notifs.service";

export const getInbox = createAsyncThunk("notifs/inbox", async (_, thunkAPI) => {
    try {
        let data = await NotifsService.getInbox();
        data = data.filter((email) => !email[1].includes("Re:"));
        return data;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const sendEmail = createAsyncThunk(
    "notifs/sendEmail",
    async ({ subject, recipient, body }, thunkAPI) => {
        try {
            const data = await NotifsService.sendEmail(recipient, subject, body);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const initialState = {
    inbox: null,
    getInboxLoading: true,
};

const notifsSlice = createSlice({
    name: "notifs",
    initialState,
    reducers: {},
    extraReducers: {
        [getInbox.pending]: (state, action) => {
            state.getInboxLoading = true;
        },
        [getInbox.fulfilled]: (state, action) => {
            state.getInboxLoading = false;
            state.inbox = action.payload;
        },
        [getInbox.rejected]: (state, action) => {
            state.getInboxLoading = false;
            toast.error("Error on retrieving inbox " + action.payload);
        },
    },
});

export const {} = notifsSlice.actions;

export default notifsSlice.reducer;
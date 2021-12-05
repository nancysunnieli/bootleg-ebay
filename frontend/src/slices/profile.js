import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { toast } from "react-toastify";
import UserService from "../services/user.service";
import { setUser } from "./auth";

const initialState = {
    visible: false,
    isSaving: false,
};

export const modifyProfile = createAsyncThunk(
    "profile/modifyProfile",
    async ({ id, email, password }, thunkAPI) => {
        console.log("Modify profile");
        try {
            const data = await UserService.modifyProfile(id, { email, password });
            thunkAPI.dispatch(setUser(data));
            thunkAPI.dispatch(setEditModalVisible(false));
            return { user: data };
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const deleteAccount = createAsyncThunk("profile/deleteAccount", async (id, thunkAPI) => {
    console.log("Delete account");
    try {
        const result = await UserService.deleteAccount(id);
        window.location.reload();
        return result;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const suspendAccount = createAsyncThunk(
    "profile/suspendAccount",
    async ({ user_id }, thunkAPI) => {
        try {
            const data = await UserService.suspendAccount(user_id);
            console.log("Susspend account data", data);
            thunkAPI.dispatch(setUser(data));
            return { user: data };
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const unsuspendAccount = createAsyncThunk(
    "profile/unsuspendAccount",
    async ({ user_id }, thunkAPI) => {
        try {
            const data = await UserService.unsuspendAccount(user_id);
            console.log("Unsuspend account data", data);
            thunkAPI.dispatch(setUser(data));
            return { user: data };
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const profileSlice = createSlice({
    name: "profile",
    initialState,
    reducers: {
        setEditModalVisible(state, action) {
            state.visible = action.payload;
        },
    },
    extraReducers: {
        [modifyProfile.pending]: (state, action) => {
            state.isSaving = true;
        },
        [modifyProfile.fulfilled]: (state, action) => {
            state.isSaving = false;
        },
        [modifyProfile.rejected]: (state, action) => {
            toast.error(`Oops, something went wrong ${action.payload}`);
        },
        [deleteAccount.pending]: (state, action) => {},
        [deleteAccount.fulfilled]: (state, action) => {},
        [deleteAccount.rejected]: (state, action) => {
            toast.error(`Oops, something went wrong ${action.payload}`);
        },
    },
});
export const { setEditModalVisible } = profileSlice.actions;

export default profileSlice.reducer;

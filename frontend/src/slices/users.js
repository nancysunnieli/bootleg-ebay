import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { FaUserSlash } from "react-icons/fa";
import { toast } from "react-toastify";
import AuctionsService from "../services/auctions.service";
import UserService from "../services/user.service";
import { setUser } from "./auth";
import { current } from "immer";
export const getUser = createAsyncThunk("users/getUser", async ({ user_id }, thunkAPI) => {
    try {
        const data = await UserService.getUserInfo(user_id);
        return data;
    } catch (error) {
        const message = error.response?.data?.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const getUserBids = createAsyncThunk("users/getUserBids", async ({ user_id }, thunkAPI) => {
    try {
        const data = await AuctionsService.getUserBids(user_id);
        return data;
    } catch (error) {
        const message = error.response?.data?.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const suspendAccount = createAsyncThunk(
    "users/suspendAccount",
    async ({ user_id }, thunkAPI) => {
        try {
            console.log("User suspend account called");
            const data = await UserService.suspendAccount(user_id);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const unsuspendAccount = createAsyncThunk(
    "users/unsuspendAccount",
    async ({ user_id }, thunkAPI) => {
        try {
            const data = await UserService.unsuspendAccount(user_id);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const initialState = {
    user: null,
    isGetUserLoading: true,
    userBids: [],
    isGetUserBidsLoading: true,
};

const usersSlice = createSlice({
    name: "users",
    initialState,
    reducers: {},
    extraReducers: {
        [getUser.pending]: (state, action) => {
            state.isGetUserLoading = true;
        },
        [getUser.fulfilled]: (state, action) => {
            state.isGetUserLoading = false;
            state.user = action.payload;
        },
        [getUser.rejected]: (state, action) => {
            state.isGetUserLoading = false;
            toast.error("Error on fetching user " + action.payload);
        },
        [getUserBids.pending]: (state, action) => {
            state.isGetUserBidsLoading = true;
        },
        [getUserBids.fulfilled]: (state, action) => {
            state.isGetUserBidsLoading = false;
            state.userBids = action.payload;
        },
        [getUserBids.rejected]: (state, action) => {
            state.isGetUserBidsLoading = false;
            toast.error("Erorr on fetching user bids " + action.payload);
        },
        [suspendAccount.pending]: (state, action) => {
            toast("Suspending user...");
        },
        [suspendAccount.fulfilled]: (state, action) => {
            toast.success("Suspended user");
            console.log("Action payload", action.payload);
            console.log(current(state));
            state.user.suspended = 1;
        },
        [suspendAccount.rejected]: (state, action) => {
            toast.error("Something went wrong when trying to suspend user " + action.payload);
        },
        [unsuspendAccount.pending]: (state, action) => {
            toast("Unsuspending user...");
        },
        [unsuspendAccount.fulfilled]: (state, action) => {
            toast.success("Unsuspended user");
            state.user.suspended = 0;
        },
        [unsuspendAccount.rejected]: (state, action) => {
            toast.error("Something went wrong when trying to unsuspend user " + action.payload);
        },
    },
});
export const {} = usersSlice.actions;

export default usersSlice.reducer;

import React, { useCallback, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import "./App.css";
import AdminDashboard from "./components/AdminDashboard/AdminDashboard";
import Auction from "./components/Auctions/Auction";
import Auctions from "./components/Auctions/Auctions";
import Cart from "./components/Cart/Cart";
import Home from "./components/Home/Home";
import CreateItem from "./components/Items/CreateItem";
import Item from "./components/Items/Item";
import Items from "./components/Items/Items";
import Login from "./components/Login/Login";
import Logout from "./components/Logout/Logout";
import NavBar from "./components/NavBar/NavBar.js";
import NotFound from "./components/NotFound/NotFound";
import Profile from "./components/Profile/Profile";
import Register from "./components/Register/Register";
import PrivateRoute from "./components/Routing/PrivateRouter";
import Splash from "./components/Splash/Splash";
import Users from "./components/Users/Users";
import { ROLE_ADMIN, ROLE_USER } from "./constants";
import { checkLocalLogin } from "./slices/auth";

const App = () => {
    const { isLoggedIn } = useSelector((state) => state.auth);
    const dispatch = useDispatch();

    const _checkLocalLogin = useCallback(() => {
        dispatch(checkLocalLogin());
    }, [dispatch]);

    useEffect(() => {
        _checkLocalLogin();
    }, [_checkLocalLogin]);

    if (isLoggedIn == null) {
        return <Splash />;
    }

    return (
        <Router>
            <div>
                <NavBar />
                <div className="container mt-3">
                    <Switch>
                        <Route exact path="/login" component={Login} />
                        <Route exact path="/register" component={Register} />
                        <Route exact path="/logout" component={Logout} />

                        <PrivateRoute
                            exact
                            path={["/", "/home"]}
                            component={Home}
                            roles={[ROLE_USER]}
                        />
                        <PrivateRoute
                            exact
                            path="/profile"
                            component={Profile}
                            roles={[ROLE_USER]}
                        />
                        <PrivateRoute exact path="/items" component={Items} roles={[ROLE_USER]} />
                        <PrivateRoute
                            path={`/items/:item_id`}
                            component={Item}
                            roles={[ROLE_USER]}
                        />
                        <PrivateRoute
                            exact
                            path="/create_item"
                            component={CreateItem}
                            roles={[ROLE_USER]}
                        />
                        <PrivateRoute
                            exact
                            path="/auctions"
                            component={Auctions}
                            roles={[ROLE_USER]}
                        />
                        <PrivateRoute
                            path={`/auctions/:auction_id`}
                            component={Auction}
                            roles={[ROLE_USER]}
                        />
                        <PrivateRoute
                            path={`/users/:user_id`}
                            component={Users}
                            roles={[ROLE_USER]}
                        />

                        <PrivateRoute exact path="/cart" component={Cart} roles={[ROLE_USER]} />
                        <PrivateRoute
                            exact
                            path="/admin"
                            component={AdminDashboard}
                            roles={[ROLE_ADMIN]}
                        />
                        <Route path="/" component={NotFound} />
                    </Switch>
                </div>
            </div>
        </Router>
    );
};

export default App;

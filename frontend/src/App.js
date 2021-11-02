import React, { useState, useEffect, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import NavBar from "react-bootstrap/NavBar";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import "./App.css";

import Login from "./components/Login/Login";
import Register from "./components/Register/Register";
import Home from "./components/Home/Home";
import Profile from "./components/Profile/Profile";
import AdminDashboard from "./components/AdminDashboard/AdminDashboard";

import { logout } from "./slices/auth";
import PrivateRoute from "./components/Routing/PrivateRouter";
import { ROLE_USER, ROLE_ADMIN } from "./constants";
import Logout from "./components/Logout/Logout";
import { useHistory } from "react-router-dom";
import Items from "./components/Items/Items";
import Auctions from "./components/Auctions/Auctions";
import Cart from "./components/Cart/Cart";
const NotFound = () => {
    return <h1>Not found</h1>;
};
const App = () => {
    const [showAdminBoard, setShowAdminBoard] = useState(false);
    const history = useHistory();
    const { user: currentUser } = useSelector((state) => state.auth);
    console.log("user", currentUser);
    const dispatch = useDispatch();

    const logOut = useCallback(() => {
        dispatch(logout());
    }, [dispatch]);

    useEffect(() => {
        if (currentUser) {
            setShowAdminBoard(currentUser.roles.includes("ROLE_ADMIN"));
        } else {
            setShowAdminBoard(false);
        }

        document.addEventListener("logout", () => {
            logOut();
        });

        return () => {
            document.removeEventListener("logout", () => {});
        };
    }, [currentUser, logOut]);

    return (
        <Router>
            <div>
                <NavBar bg="light" expand="lg">
                    <Container>
                        <NavBar.Brand as={Link} to={"/home"}>
                            Bootleg Ebay
                        </NavBar.Brand>
                        <NavBar.Toggle aria-controls="basic-navbar-nav" />
                        <NavBar.Collapse id="basic-navbar-nav">
                            <Nav className="me-auto">
                                {currentUser && [
                                    <Nav.Link as={Link} to="/home" key={0}>
                                        Home
                                    </Nav.Link>,
                                    <Nav.Link as={Link} to="/profile" key={1}>
                                        Profile
                                    </Nav.Link>,
                                    <Nav.Link as={Link} to="/items" key={2}>
                                        Items
                                    </Nav.Link>,
                                    <Nav.Link as={Link} to="/auctions" key={3}>
                                        Auctions
                                    </Nav.Link>,
                                ]}
                                {currentUser ? (
                                    <Nav.Link as={Link} to="/logout">
                                        Logout
                                    </Nav.Link>
                                ) : (
                                    [
                                        <Nav.Link as={Link} to="/login" key={0}>
                                            Login
                                        </Nav.Link>,
                                        <Nav.Link as={Link} to="/register" key={1}>
                                            Register
                                        </Nav.Link>,
                                    ]
                                )}
                                {showAdminBoard && (
                                    <Nav.Link as={Link} to="/admin">
                                        Admin
                                    </Nav.Link>
                                )}
                            </Nav>
                            {currentUser && (
                                <Nav>
                                    <Nav.Link as={Link} to="/cart">
                                        Cart
                                    </Nav.Link>
                                </Nav>
                            )}
                        </NavBar.Collapse>
                    </Container>
                </NavBar>

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
                            exact
                            path="/auctions"
                            component={Auctions}
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

import { useState, useEffect } from "react";
import Nav from "react-bootstrap/Nav";
import NavBar from "react-bootstrap/Navbar";
import { useSelector } from "react-redux";
import Container from "react-bootstrap/Container";
import { Link } from "react-router-dom";
import Badge from "react-bootstrap/Badge";
import { FaShoppingCart } from "react-icons/fa";
import "./NavBar.css";
export default function Navbar() {
    const [showAdminBoard, setShowAdminBoard] = useState(false);
    const { user: currentUser, isLoggedIn } = useSelector((state) => state.auth);
    const { cartItems } = useSelector((state) => state.cart);

    useEffect(() => {
        if (currentUser) {
            setShowAdminBoard(!!currentUser.is_admin);
        } else {
            setShowAdminBoard(false);
        }
    }, [currentUser]);

    return (
        <NavBar bg="light" expand="lg">
            <Container>
                <NavBar.Brand as={Link} to={"/home"} className="logo">
                    <div>Bootleg Ebay</div>
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
                        {isLoggedIn ? (
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
                        <Nav style={{ alignItems: "center" }}>
                            <Nav.Link as={Link} to="/cart">
                                <Badge pill bg="info">
                                    <FaShoppingCart /> Cart{" "}
                                    {cartItems.length > 0 && cartItems.length}
                                </Badge>
                            </Nav.Link>
                        </Nav>
                    )}
                </NavBar.Collapse>
            </Container>
        </NavBar>
    );
}

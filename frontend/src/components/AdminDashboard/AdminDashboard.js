import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getCategories, getFlaggedItems, removeCategory } from "../../slices/items";
import Spinner from "react-bootstrap/Spinner";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import ModifyCategoryModal from "./ModifyCategoryModal";
import CreateCategoryModal from "../Items/CreateCategoryModal";
import FlaggedItems from "./FlaggedItems";
import ButtonGroup from "react-bootstrap/ButtonGroup";
// import DropdownButton from "react-bootstrap/DropdownButton";
import Dropdown from "react-bootstrap/Dropdown";
import { getAuctionMetrics } from "../../slices/auctions";
export default function AdminDashboard() {
    const { categories } = useSelector((state) => state.items);
    const { getAuctionMetricsLoading, auctionMetrics } = useSelector((state) => state.auctions);
    const dispatch = useDispatch();
    const [selectedCategory, setSelectedCategory] = useState("");
    const [showModifyCategoryModal, setShowModifyCategoryModal] = useState(false);
    const [showCreateCategoryModal, setShowCreateCategoryModal] = useState(false);
    const [mode, setMode] = useState(null);

    useEffect(() => {
        dispatch(getCategories());
    }, []);

    const handleCategoryEdit = (category) => {
        setSelectedCategory(category);
        setShowModifyCategoryModal(true);
    };
    const handleCategoryDelete = (category) => {
        dispatch(removeCategory({ category }));
    };

    const handleViewMetrics = (mode) => {
        let now = Math.floor(new Date().getTime() / 1000);
        if (mode === 1) {
            setMode("Last Day");
            dispatch(getAuctionMetrics({ end: now, start: now - 24 * 60 * 60 }));
        } else if (mode === 2) {
            setMode("Last Week");
            dispatch(getAuctionMetrics({ end: now, start: now - 604800 }));
        } else {
            setMode("Last Month");
            dispatch(getAuctionMetrics({ end: now, start: now - 2592000 }));
        }
    };

    console.log("metrics", auctionMetrics);
    return (
        <div>
            <h1>Admin Dashboard</h1>
            <br />
            <h2>Flagged Items</h2>
            {/* <FlaggedItems /> */}

            <br />
            <hr />
            <br />
            <h2>Categories</h2>
            <br />
            <div>
                <Button onClick={() => setShowCreateCategoryModal(true)}>Add Category</Button>
            </div>
            <br />
            <div style={{ maxWidth: "60%" }}>
                {categories.length ? (
                    <ListGroup>
                        {categories.map((category) => (
                            <ListGroup.Item key={category}>
                                <Row>
                                    <Col>{category}</Col>
                                    <Col md="auto">
                                        <Button
                                            variant="info"
                                            onClick={() => handleCategoryEdit(category)}
                                        >
                                            Edit
                                        </Button>
                                    </Col>
                                    <Col md="auto">
                                        <Button
                                            variant="danger"
                                            onClick={() => handleCategoryDelete(category)}
                                        >
                                            Delete
                                        </Button>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                        ))}
                    </ListGroup>
                ) : (
                    <Spinner animation="grow" variant="success" />
                )}
            </div>
            <ModifyCategoryModal
                show={showModifyCategoryModal}
                handleClose={() => setShowModifyCategoryModal(false)}
                category={selectedCategory}
            />
            <CreateCategoryModal
                show={showCreateCategoryModal}
                handleClose={() => setShowCreateCategoryModal(false)}
            />

            <br />
            <hr />
            <br />
            <h2>Auction Metrics</h2>
            <br />
            <Dropdown title="Dropdown">
                <Dropdown.Toggle variant="info" id="dropdown-basic">
                    View Metrics For {mode}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                    <Dropdown.Item eventKey="1" onClick={() => handleViewMetrics(1)}>
                        Last day
                    </Dropdown.Item>
                    <Dropdown.Item eventKey="2" onClick={() => handleViewMetrics(2)}>
                        Last week
                    </Dropdown.Item>
                    <Dropdown.Item eventKey="3" onClick={() => handleViewMetrics(3)}>
                        Last month
                    </Dropdown.Item>
                </Dropdown.Menu>
            </Dropdown>
            {getAuctionMetricsLoading ? (
                <Spinner animation="grow" variant="success" />
            ) : (
                <p>{JSON.stringify(auctionMetrics)}</p>
            )}

            <br />
            <hr />
            <br />
            <h2>Customer Support Emails</h2>
            <br />

            {/* View auction metrics */}
            {/* Examine emails received by customer support */}
            {/*  */}
            <br />
        </div>
    );
}

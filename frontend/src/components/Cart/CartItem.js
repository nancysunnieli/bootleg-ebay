import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import { FaTimes } from "react-icons/fa";
import { useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import "./cart.css";
export default function CartItem({ item, handleDeleteItem }) {
    const {
        _id,
        available,
        category,
        description,
        isFlagged,
        name,
        photos,
        price,
        sellerID,
        watchlist,
    } = item.item;

    const dispatch = useDispatch;

    return (
        <Card style={{ minWidth: "650px" }}>
            <Card.Header as="h5">
                {name}
                <span className="timesIcon" onClick={() => handleDeleteItem(item.item)}>
                    <FaTimes />
                </span>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md="auto">
                        <Card.Img
                            style={{ height: "10rem", width: "auto" }}
                            variant="top"
                            src={`data:image/png;base64, ${photos}`}
                        />
                    </Col>
                    <Col md="8">
                        <Card.Text>{description}</Card.Text>
                    </Col>
                    <Col>
                        <Row>
                            <Card.Text>${price}</Card.Text>
                        </Row>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    );
}

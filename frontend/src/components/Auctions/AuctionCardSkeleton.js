import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Badge from "react-bootstrap/Badge";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Row from "react-bootstrap/Row";
import useInterval from "../../hooks/useInterval";
import moment from "moment";
import { useState } from "react";
const Auction = ({ auction, item }) => {
    const { auction_id, bids, end_time, item_id, seller_id, start_time } = auction;
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
    } = item;

    const [timeNow, setTimeNow] = useState(new Date());

    useInterval(() => {
        setTimeNow(new Date());
    }, 1000);

    let remainingDuration = end_time * 1000 - timeNow.getTime();
    let timeRemaining = moment.utc(remainingDuration).format("D [days,] HH:mm:ss");
    return (
        <Col>
            <Card>
                <Card.Img variant="top" src={`https://picsum.photos/378/160?${_id}`} />
                <Card.Body>
                    <Card.Title>{name}</Card.Title>
                    <Card.Text>Auction ends in {timeRemaining}</Card.Text>
                    <Card.Text>{description}</Card.Text>
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <Card.Text>${price}</Card.Text>
                        <Card.Text>{bids.length} bids</Card.Text>
                        <Button variant="success">Buy Now</Button>{" "}
                        <Button variant="info">Bid</Button>
                    </div>
                </Card.Body>
                <Card.Footer>
                    <Row>
                        {category.map((c, i) => (
                            <Col md="auto">
                                <Badge key={i} bg="primary">
                                    {c}
                                </Badge>
                            </Col>
                        ))}
                    </Row>
                </Card.Footer>
            </Card>
        </Col>
    );
};

export default Auction;

import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Badge from "react-bootstrap/Badge";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Row from "react-bootstrap/Row";
import useInterval from "../../hooks/useInterval";
import moment from "moment";
import { useCallback, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addItemToCart } from "../../slices/cart";
import { useHistory } from "react-router-dom";

function convertRemToPixels(rem) {
    return rem * parseFloat(getComputedStyle(document.documentElement).fontSize);
}

const imageHeight = convertRemToPixels(15);
console.log(imageHeight);

const Auction = ({ auction, item, isBuyNowDisabled }) => {
    const { auction_id, bids, end_time, item_id, seller_id, start_time } = auction;
    const { _id, category, description, isFlagged, name, photos, price, sellerID, watchlist } =
        item;

    const [timeNow, setTimeNow] = useState(new Date());
    const { user } = useSelector((state) => state.auth);
    const history = useHistory();
    const dispatch = useDispatch();
    const buyNow = useCallback(() => {
        dispatch(addItemToCart({ item, user_id: user.user_id }));
    }, [dispatch]);

    const bidNow = useCallback(() => {
        history.push(`/auctions/${auction_id}`);
    }, [history]);

    useInterval(() => {
        setTimeNow(new Date());
    }, 1000);

    let remainingDuration = Math.min(end_time * 1000 - timeNow.getTime());
    let timeRemaining = moment.utc(remainingDuration).format("D [days,] HH:mm:ss");
    return (
        <Col>
            <Card onClick={bidNow} style={{ zIndex: 1 }}>
                <Card.Img
                    variant="top"
                    src={`data:image/png;base64, ${photos}`}
                    style={{ maxHeight: `15rem`, height: "auto", width: "auto", display: "block" }}
                />
                <Card.Body>
                    <Card.Title>{name}</Card.Title>
                    <Card.Text>Auction ends in {timeRemaining}</Card.Text>
                    <Card.Text>{description}</Card.Text>
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                        }}
                    >
                        <Button
                            variant="warning"
                            onClick={buyNow}
                            disabled={remainingDuration === 0}
                            disabled={isBuyNowDisabled}
                        >
                            Buy Now ${price}
                        </Button>
                        <Button
                            style={{ zIndex: 100 }}
                            variant="info"
                            disabled={remainingDuration === 0}
                            onClick={bidNow}
                        >
                            Bid ({bids.length} bids)
                        </Button>
                    </div>
                </Card.Body>
                <Card.Footer>
                    <Row>
                        {category.map((c, i) => (
                            <Col md="auto" key={i}>
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

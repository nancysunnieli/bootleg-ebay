import { useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import NotFound from "../NotFound/NotFound";

export default function Auction() {
    const { auction_id } = useParams();
    const { auctions } = useSelector((state) => state.auctions);
    const auction = auctions.find((auction) => auction.auction.auction_id === auction_id);
    console.log("auction", auction, auctions, auction_id);
    if (auction === undefined) {
        return <NotFound />;
    }

    return (
        <div>
            <div>{auction_id}</div>
            <div>{JSON.stringify(auction)}</div>
        </div>
    );
}

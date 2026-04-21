import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";

patch(ReceiptScreen.prototype, {
    async downloadImage() {
        const imageBase64 = await this.generateTicketImage();
        const blob = new Blob(
            [Uint8Array.from(atob(imageBase64), (c) => c.charCodeAt(0))],
            { type: "image/jpeg" }
        );
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `recibo_${this.pos.get_order().name}.jpg`;
        a.click();
        URL.revokeObjectURL(url);
    },
});

import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectPartnerButton } from "@point_of_sale/app/screens/product_screen/control_buttons/select_partner_button/select_partner_button";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { _t } from "@web/core/l10n/translation";
import { useAsyncLockedMethod } from "@point_of_sale/app/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { QuotationScreen } from "@pi_pos_receipt_custom/js/quotation_screen";

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.clickPrintQuotation = useAsyncLockedMethod(this.clickPrintQuotation);
    },
    async clickPrintQuotation() {
        // Need to await to have the result in case of automatic skip screen.
        (await this.printer.print(OrderReceipt, {
            data: this.pos.orderExportForPrinting(this.pos.get_order()),
            formatCurrency: this.env.utils.formatCurrency,
        })) || this.dialog.add(QuotationScreen);
    }
});
patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectPartnerButton,
    },
});
